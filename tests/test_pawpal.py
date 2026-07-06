"""Basic tests for the PawPal+ backend classes."""

from datetime import datetime

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
