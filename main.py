"""CLI demo for PawPal+.

Builds a small owner/pets/tasks setup and prints a schedule using Scheduler.
Run with: python main.py
"""

from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo() -> Owner:
    """Create a sample owner with two pets and a few tasks for today."""
    owner = Owner(name="Jordan", email="jordan@example.com")

    milo = Pet(name="Milo", species="dog", age=4)
    luna = Pet(name="Luna", species="cat", age=2)
    owner.add_pet(milo)
    owner.add_pet(luna)

    today = datetime.now()

    milo.add_task(
        Task("Feed breakfast", today.replace(hour=9, minute=0), priority=1)
    )
    milo.add_task(
        Task("Evening walk", today.replace(hour=17, minute=0), priority=2)
    )
    luna.add_task(
        Task("Give medication", today.replace(hour=12, minute=30), priority=1)
    )
    luna.add_task(
        Task("Vet check-up", today.replace(hour=10, minute=0) + timedelta(days=1), priority=2)
    )

    return owner


def main() -> None:
    """Print today's schedule, sorted by due time, across all pets."""
    owner = build_demo()
    scheduler = Scheduler(owner)

    print("Today's Schedule")
    print("----------------")
    todays_tasks = scheduler.sort_tasks_by_due_time()
    todays_tasks = [pair for pair in todays_tasks if pair[1].is_due_today()]
    print(scheduler.format_schedule(todays_tasks))


if __name__ == "__main__":
    main()
