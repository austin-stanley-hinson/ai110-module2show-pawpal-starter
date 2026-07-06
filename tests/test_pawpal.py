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
