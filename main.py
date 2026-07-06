"""CLI demo for PawPal+.

Shows the scheduler algorithms: sorting, filtering, recurring tasks, and
conflict detection across multiple pets. Run with: python main.py
"""

from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo() -> Owner:
    """Create an owner with two pets and tasks that exercise the scheduler."""
    owner = Owner(name="Jordan", email="jordan@example.com")

    milo = Pet(name="Milo", species="dog", age=4)
    luna = Pet(name="Luna", species="cat", age=2)
    owner.add_pet(milo)
    owner.add_pet(luna)

    today = datetime.now()

    def at(hour: int, minute: int = 0) -> datetime:
        return today.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # Added out of due-time order on purpose so sorting is visibly useful.
    milo.add_task(Task("Evening walk", at(17, 0), priority=2))
    milo.add_task(Task("Feed breakfast", at(8, 0), priority=1, frequency="daily"))
    luna.add_task(Task("Give medication", at(12, 30), priority=1))

    # Two tasks at the EXACT same time (one per pet) to demo conflict detection.
    milo.add_task(Task("Vet call", at(15, 0), priority=3))
    luna.add_task(Task("Grooming", at(15, 0), priority=2))

    return owner


def print_pairs(pairs) -> None:
    """Print (pet, task) pairs in a readable one-line-per-task format."""
    if not pairs:
        print("(none)")
        return
    for pet, task in pairs:
        status = "Complete" if task.completed else "Incomplete"
        time_str = task.due_at.strftime("%I:%M %p")
        print(
            f"{time_str} | {pet.name} | {task.description} | "
            f"Priority {task.priority} | {task.frequency} | {status}"
        )


def main() -> None:
    """Run the scheduler demo and print each algorithmic feature."""
    owner = build_demo()
    scheduler = Scheduler(owner)

    print("Today's Schedule")
    print("----------------")
    print_pairs(scheduler.tasks_due_today())

    print("\nSorted Schedule (by due time)")
    print("-----------------------------")
    print_pairs(scheduler.sort_tasks_by_due_time())

    print("\nIncomplete Tasks for Milo")
    print("-------------------------")
    print_pairs(scheduler.filter_tasks(pet_name="Milo", completed=False))

    print("\nRecurring Task Demo")
    print("-------------------")
    completed, next_task = scheduler.complete_task("Milo", "Feed breakfast")
    if completed is not None:
        print(f"Completed: {completed.description} for Milo.")
    if next_task is not None:
        print(
            f"Next occurrence created: {next_task.description} on "
            f"{next_task.due_at.strftime('%b %d %I:%M %p')} ({next_task.frequency})."
        )

    print("\nConflict Warnings")
    print("-----------------")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("No conflicts found.")


if __name__ == "__main__":
    main()
