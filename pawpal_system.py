"""PawPal+ logic layer (Phase 1 skeleton).

These class stubs match diagrams/uml_draft.mmd. Method bodies are left as
`pass` on purpose because this phase only covers the design/skeleton.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """A single care task for a pet (walk, feeding, meds, etc.)."""

    description: str
    due_at: datetime
    completed: bool = False
    priority: str = "medium"

    def mark_complete(self) -> None:
        """Mark this task as done."""
        pass

    def is_due_today(self) -> bool:
        """Return True if this task is due on today's date."""
        pass


@dataclass
class Pet:
    """A pet that belongs to an owner and has a list of care tasks."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        pass

    def list_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        pass

    def get_incomplete_tasks(self) -> list[Task]:
        """Return only the tasks that are not completed yet."""
        pass


@dataclass
class Owner:
    """The pet owner, who can have multiple pets."""

    name: str
    email: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's profile."""
        pass

    def list_pets(self) -> list[Pet]:
        """Return all pets owned by this owner."""
        pass

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        pass


class Scheduler:
    """Organizes tasks across all pets that belong to a single owner."""

    def __init__(self, owner: Owner) -> None:
        """Store the owner whose pets and tasks this scheduler manages."""
        self.owner = owner

    def get_all_tasks(self) -> list[Task]:
        """Collect tasks from every pet the owner has."""
        pass

    def sort_tasks_by_due_time(self) -> list[Task]:
        """Return all tasks ordered by their due time."""
        pass

    def filter_incomplete_tasks(self) -> list[Task]:
        """Return only tasks that still need to be done."""
        pass

    def tasks_due_today(self) -> list[Task]:
        """Return the tasks that are due today across all pets."""
        pass
