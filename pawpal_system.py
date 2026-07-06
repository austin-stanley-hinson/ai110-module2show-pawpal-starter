"""PawPal+ logic layer.

Working backend classes for the PawPal+ pet care planner: Task, Pet, Owner,
and a Scheduler that organizes tasks across all of an owner's pets.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class Task:
    """A single care task for a pet (walk, feeding, meds, etc.)."""

    description: str
    due_at: datetime
    completed: bool = False
    priority: int = 3
    frequency: str = "once"

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def is_due_today(self, current_time: datetime | None = None) -> bool:
        """Return True if this task is due on the same calendar date as now."""
        if current_time is None:
            current_time = datetime.now()
        return self.due_at.date() == current_time.date()

    def create_next_occurrence(self) -> "Task | None":
        """Return the next recurring Task (daily/weekly), or None if not recurring."""
        if self.frequency == "daily":
            next_due = self.due_at + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due = self.due_at + timedelta(weeks=1)
        else:
            return None
        return Task(
            description=self.description,
            due_at=next_due,
            completed=False,
            priority=self.priority,
            frequency=self.frequency,
        )

    def __str__(self) -> str:
        """Human-readable one-line summary of the task."""
        status = "Complete" if self.completed else "Incomplete"
        time_str = self.due_at.strftime("%I:%M %p")
        return f"{time_str} | {self.description} | Priority {self.priority} | {status}"


@dataclass
class Pet:
    """A pet that belongs to an owner and has a list of care tasks."""

    name: str
    species: str
    age: int | None = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def list_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def get_incomplete_tasks(self) -> list[Task]:
        """Return only the tasks that are not completed yet."""
        return [task for task in self.tasks if not task.completed]

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task complete; if it recurs, add and return the next occurrence."""
        task.mark_complete()
        next_task = task.create_next_occurrence()
        if next_task is not None:
            self.add_task(next_task)
        return next_task


@dataclass
class Owner:
    """The pet owner, who can have multiple pets."""

    name: str
    email: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's profile."""
        self.pets.append(pet)

    def list_pets(self) -> list[Pet]:
        """Return all pets owned by this owner."""
        return self.pets

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return (pet, task) pairs for every task across every pet."""
        pairs = []
        for pet in self.pets:
            for task in pet.list_tasks():
                pairs.append((pet, task))
        return pairs


class Scheduler:
    """Organizes tasks across all pets that belong to a single owner."""

    def __init__(self, owner: Owner) -> None:
        """Store the owner whose pets and tasks this scheduler manages."""
        self.owner = owner

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Collect (pet, task) pairs from every pet the owner has."""
        return self.owner.get_all_tasks()

    def sort_tasks_by_due_time(self) -> list[tuple[Pet, Task]]:
        """Return all (pet, task) pairs ordered by their due time."""
        return sorted(self.get_all_tasks(), key=lambda pair: pair[1].due_at)

    def filter_incomplete_tasks(self) -> list[tuple[Pet, Task]]:
        """Return only the (pet, task) pairs that still need to be done."""
        return [pair for pair in self.get_all_tasks() if not pair[1].completed]

    def filter_tasks(
        self, pet_name: str | None = None, completed: bool | None = None
    ) -> list[tuple[Pet, Task]]:
        """Return (pet, task) pairs filtered by pet name and/or completion status."""
        results = []
        for pet, task in self.get_all_tasks():
            if pet_name is not None and pet.name.lower() != pet_name.lower():
                continue
            if completed is not None and task.completed != completed:
                continue
            results.append((pet, task))
        return results

    def detect_conflicts(self) -> list[str]:
        """Return warning strings for tasks that share the exact same due_at time."""
        by_time: dict[datetime, list[tuple[Pet, Task]]] = {}
        for pet, task in self.get_all_tasks():
            by_time.setdefault(task.due_at, []).append((pet, task))

        warnings = []
        for due_at, pairs in by_time.items():
            if len(pairs) > 1:
                time_str = due_at.strftime("%b %d %I:%M %p")
                details = ", ".join(f"{pet.name}: {task.description}" for pet, task in pairs)
                warnings.append(f"Conflict at {time_str} -> {details}")
        return warnings

    def complete_task(
        self, pet_name: str, task_description: str
    ) -> tuple[Task | None, Task | None]:
        """Complete the first matching incomplete task; return (completed, next) tasks."""
        for pet, task in self.get_all_tasks():
            if (
                pet.name.lower() == pet_name.lower()
                and task.description == task_description
                and not task.completed
            ):
                next_task = pet.complete_task(task)
                return task, next_task
        return None, None

    def tasks_due_today(self, current_time: datetime | None = None) -> list[tuple[Pet, Task]]:
        """Return the (pet, task) pairs due today across all pets."""
        return [
            pair for pair in self.get_all_tasks() if pair[1].is_due_today(current_time)
        ]

    def format_schedule(self, tasks: list[tuple[Pet, Task]] | None = None) -> str:
        """Build a readable multi-line schedule string from (pet, task) pairs."""
        if tasks is None:
            tasks = self.sort_tasks_by_due_time()
        if not tasks:
            return "No tasks scheduled."
        lines = []
        for pet, task in tasks:
            status = "Complete" if task.completed else "Incomplete"
            time_str = task.due_at.strftime("%I:%M %p")
            lines.append(
                f"{time_str} | {pet.name} | {task.description} | "
                f"Priority {task.priority} | {status}"
            )
        return "\n".join(lines)
