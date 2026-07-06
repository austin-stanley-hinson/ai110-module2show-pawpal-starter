"""Tests for the PawPal+ backend classes.

Test plan (behavior, not print output):
1. Task completion      -> mark_complete() flips completed False -> True
2. Pet task management   -> add_task() adds a task to the pet's list
3. Scheduler sorting     -> out-of-order tasks come back in chronological order
4. Recurrence logic      -> completing a daily task creates next day's task
5. Conflict detection    -> two tasks at the same due_at are flagged
6. Edge cases            -> empty owner doesn't break scheduler methods,
                            "once" tasks don't recur, filtering by pet name is
                            case-insensitive, no conflicts returns an empty list
"""

from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete():
    """Completing a task should flip its completed flag to True."""
    task = Task("Feed breakfast", datetime(2026, 7, 6, 9, 0))
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_to_pet():
    """Adding a task to a pet should grow its task list and contain the task."""
    pet = Pet(name="Milo", species="dog", age=4)
    task = Task("Evening walk", datetime(2026, 7, 6, 17, 0))
    assert len(pet.list_tasks()) == 0
    pet.add_task(task)
    assert len(pet.list_tasks()) == 1
    assert task in pet.list_tasks()


def test_scheduler_sorts_by_due_time():
    """Scheduler should return tasks across pets ordered by due time."""
    owner = Owner(name="Jordan", email="jordan@example.com")
    milo = Pet(name="Milo", species="dog", age=4)
    luna = Pet(name="Luna", species="cat", age=2)
    owner.add_pet(milo)
    owner.add_pet(luna)

    milo.add_task(Task("Evening walk", datetime(2026, 7, 6, 17, 0)))
    luna.add_task(Task("Give medication", datetime(2026, 7, 6, 12, 30)))
    milo.add_task(Task("Feed breakfast", datetime(2026, 7, 6, 9, 0)))

    scheduler = Scheduler(owner)
    ordered = scheduler.sort_tasks_by_due_time()

    descriptions = [task.description for _, task in ordered]
    assert descriptions == ["Feed breakfast", "Give medication", "Evening walk"]


def _two_pet_owner():
    """Helper: owner with two pets used by the filter/conflict tests."""
    owner = Owner(name="Jordan", email="jordan@example.com")
    milo = Pet(name="Milo", species="dog", age=4)
    luna = Pet(name="Luna", species="cat", age=2)
    owner.add_pet(milo)
    owner.add_pet(luna)
    return owner, milo, luna


def test_filter_tasks_by_pet_and_status():
    """filter_tasks should narrow results by pet name and completion status."""
    owner, milo, luna = _two_pet_owner()
    milo.add_task(Task("Feed breakfast", datetime(2026, 7, 6, 9, 0)))
    milo.add_task(Task("Evening walk", datetime(2026, 7, 6, 17, 0), completed=True))
    luna.add_task(Task("Give medication", datetime(2026, 7, 6, 12, 30)))

    scheduler = Scheduler(owner)

    milo_only = scheduler.filter_tasks(pet_name="milo")
    assert {task.description for _, task in milo_only} == {"Feed breakfast", "Evening walk"}

    incomplete = scheduler.filter_tasks(completed=False)
    assert {task.description for _, task in incomplete} == {"Feed breakfast", "Give medication"}


def test_recurring_task_creates_next_occurrence():
    """Completing a daily task should add a next occurrence one day later."""
    pet = Pet(name="Milo", species="dog", age=4)
    task = Task("Feed breakfast", datetime(2026, 7, 6, 8, 0), frequency="daily")
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_at == datetime(2026, 7, 7, 8, 0)
    assert len(pet.list_tasks()) == 2


def test_detect_conflicts_on_same_due_time():
    """detect_conflicts should flag two tasks scheduled at the exact same time."""
    owner, milo, luna = _two_pet_owner()
    same_time = datetime(2026, 7, 6, 15, 0)
    milo.add_task(Task("Vet call", same_time))
    luna.add_task(Task("Grooming", same_time))
    luna.add_task(Task("Give medication", datetime(2026, 7, 6, 12, 30)))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert isinstance(conflicts[0], str)


def test_sorted_due_at_values_are_ascending():
    """Sorted schedule should have non-decreasing due_at values."""
    owner, milo, luna = _two_pet_owner()
    milo.add_task(Task("Evening walk", datetime(2026, 7, 6, 17, 0)))
    luna.add_task(Task("Give medication", datetime(2026, 7, 6, 12, 30)))
    milo.add_task(Task("Feed breakfast", datetime(2026, 7, 6, 9, 0)))

    scheduler = Scheduler(owner)
    due_times = [task.due_at for _, task in scheduler.sort_tasks_by_due_time()]

    assert due_times == sorted(due_times)


def test_scheduler_complete_task_creates_recurrence():
    """Scheduler.complete_task should complete the task and return the next one."""
    owner, milo, _ = _two_pet_owner()
    milo.add_task(Task("Feed breakfast", datetime(2026, 7, 6, 8, 0), frequency="daily"))

    scheduler = Scheduler(owner)
    completed, next_task = scheduler.complete_task("MILO", "Feed breakfast")

    assert completed is not None
    assert completed.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_at == datetime(2026, 7, 6, 8, 0) + timedelta(days=1)


def test_once_task_does_not_recur():
    """A one-time task should not generate a next occurrence."""
    task = Task("Vet check-up", datetime(2026, 7, 6, 10, 0), frequency="once")
    assert task.create_next_occurrence() is None


def test_empty_owner_scheduler_methods_do_not_break():
    """Scheduler methods should work on an owner with no pets/tasks."""
    owner = Owner(name="Jordan", email="jordan@example.com")
    scheduler = Scheduler(owner)

    assert scheduler.get_all_tasks() == []
    assert scheduler.sort_tasks_by_due_time() == []
    assert scheduler.filter_tasks() == []
    assert scheduler.filter_incomplete_tasks() == []
    assert scheduler.detect_conflicts() == []
    assert scheduler.tasks_due_today() == []


def test_no_conflicts_returns_empty_list():
    """Distinct due times across pets should report no conflicts."""
    owner, milo, luna = _two_pet_owner()
    milo.add_task(Task("Feed breakfast", datetime(2026, 7, 6, 9, 0)))
    luna.add_task(Task("Give medication", datetime(2026, 7, 6, 12, 30)))

    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []
