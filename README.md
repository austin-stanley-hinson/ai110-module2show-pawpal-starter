# PawPal+ (Module 2 Project)

## Project Overview

**PawPal+** is a pet care planning assistant for a busy pet owner. It lets you add your pets, schedule care tasks for each one (walks, feeding, meds, grooming, etc.), and see everything in a single schedule sorted by time. The `Scheduler` pulls tasks together across all of your pets, supports simple daily/weekly recurring tasks, and warns you when two tasks are booked for the exact same time. It runs both as a Streamlit web app and as a command-line demo.

## Features

- Add pets to an owner profile (name, species, age)
- Schedule care tasks for a selected pet (description, due date/time, priority, frequency)
- View a schedule sorted by due time across all pets
- Filter tasks by pet and/or completion status
- Daily and weekly recurring tasks that roll over when completed
- Conflict warnings when two tasks share the exact same time
- Streamlit UI (`app.py`) and a CLI demo (`main.py`)
- Pytest test suite covering the core behaviors

## Running the Project

Install dependencies, then run either entry point:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Streamlit web app:

```bash
streamlit run app.py
```

Command-line demo:

```bash
python3 main.py
```

## Class Design

The logic layer lives in `pawpal_system.py` and has four classes (see `diagrams/uml_final.mmd`):

- **Task** — one care item. Holds `description`, `due_at`, `completed`, `priority`, and `frequency`. Can `mark_complete()`, `is_due_today()`, and `create_next_occurrence()` for recurring tasks.
- **Pet** — a single animal with `name`, `species`, `age`, and its own `tasks` list. Can `add_task()`, `list_tasks()`, `get_incomplete_tasks()`, and `complete_task()` (which also adds the next recurring occurrence).
- **Owner** — the person using the app. Holds `name`, `email`, and a list of `pets`. Can `add_pet()`, `list_pets()`, and `get_all_tasks()` (returns `(pet, task)` pairs across every pet).
- **Scheduler** — takes an `Owner` and works across all of that owner's pets. Handles the algorithmic behavior: sorting, filtering, conflict detection, and completing tasks. It is kept separate from `Owner`/`Pet` so the "figure out the plan" logic isn't crammed into the data classes.

## 🖥️ Sample Output

Running `python3 main.py` shows sorting, filtering, recurring tasks, and conflict detection (times come from "today" so they'll match the day you run it):

```
Today's Schedule
----------------
05:00 PM | Milo | Evening walk | Priority 2 | once | Incomplete
08:00 AM | Milo | Feed breakfast | Priority 1 | daily | Incomplete
03:00 PM | Milo | Vet call | Priority 3 | once | Incomplete
12:30 PM | Luna | Give medication | Priority 1 | once | Incomplete
03:00 PM | Luna | Grooming | Priority 2 | once | Incomplete

Sorted Schedule (by due time)
-----------------------------
08:00 AM | Milo | Feed breakfast | Priority 1 | daily | Incomplete
12:30 PM | Luna | Give medication | Priority 1 | once | Incomplete
03:00 PM | Milo | Vet call | Priority 3 | once | Incomplete
03:00 PM | Luna | Grooming | Priority 2 | once | Incomplete
05:00 PM | Milo | Evening walk | Priority 2 | once | Incomplete

Incomplete Tasks for Milo
-------------------------
05:00 PM | Milo | Evening walk | Priority 2 | once | Incomplete
08:00 AM | Milo | Feed breakfast | Priority 1 | daily | Incomplete
03:00 PM | Milo | Vet call | Priority 3 | once | Incomplete

Recurring Task Demo
-------------------
Completed: Feed breakfast for Milo.
Next occurrence created: Feed breakfast on Jul 07 08:00 AM (daily).

Conflict Warnings
-----------------
Conflict at Jul 06 03:00 PM -> Milo: Vet call, Luna: Grooming
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite from the repo root:
python3 -m pytest
```

The 11 tests in `tests/test_pawpal.py` cover:

- **Task completion** — `mark_complete()` flips `completed` to True.
- **Adding tasks to pets** — `add_task()` grows a pet's task list.
- **Scheduler sorting** — out-of-order tasks come back in chronological order (checked by description order and by ascending `due_at`).
- **Recurring task behavior** — completing a daily task (via `Pet.complete_task()` and `Scheduler.complete_task()`) creates the next day's task, and a `once` task does not recur.
- **Conflict detection** — two tasks at the same `due_at` are flagged, and distinct times return an empty list.
- **Edge cases** — filtering by pet name (case-insensitive) and completion status, plus an empty owner not breaking any scheduler method.

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/austinstanleyhinson/Desktop/AI-110/ai110-module2show-pawpal-starter
collected 11 items

tests/test_pawpal.py ...........                                         [100%]

============================== 11 passed in 0.02s ===============================
```

**Confidence Level: ★★★★☆**

I'd give the system 4 out of 5 stars for reliability right now. The main object interactions and the scheduling algorithms are covered by automated tests, including sorting, recurring tasks, and conflict detection, plus a few edge cases like an empty owner. I'm not giving it 5 stars yet because everything is in-memory session data with no persistence, and I haven't covered every possible user input edge case (like weird times or bad input from the UI).

## 📐 Smarter Scheduling

The `Scheduler` works across every pet the owner has (not just one). Each feature maps to a method:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_tasks_by_due_time()` | Returns all `(pet, task)` pairs sorted chronologically by `due_at`. |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)`, `Scheduler.filter_incomplete_tasks()` | Filter by pet name (case-insensitive) and/or completion status. |
| Recurring tasks | `Task.create_next_occurrence()`, `Pet.complete_task()`, `Scheduler.complete_task()` | Completing a `daily`/`weekly` task auto-adds the next occurrence (`once` returns none). |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags tasks that share the exact same `due_at`. Only exact-time matches (no duration field yet). |

## 📸 Demo Walkthrough

The Streamlit app (`streamlit run app.py`) walks through the core scheduler behavior:

1. **Set the owner.** Enter an owner name and email at the top. The `Owner` object is kept in `st.session_state`, so your pets and tasks don't disappear when Streamlit reruns the script.
2. **Add a pet.** Fill in name, species, and age, then click *Add pet*. This calls `Owner.add_pet()` with a real `Pet`, and you'll see a success message and the pet in the "Current Pets" table.
3. **Schedule a task.** Pick a pet, type a description, choose a due date + time, priority, and frequency (once/daily/weekly), then click *Add task*. This builds a real `Task` and calls `Pet.add_task()`.
4. **View the sorted schedule.** The "Schedule" section uses `Scheduler.sort_tasks_by_due_time()` to show every task across all pets in time order, rendered as a table (not raw objects).
5. **Filter.** Narrow the schedule by pet and/or completion status using `Scheduler.filter_tasks(...)`.
6. **See conflict warnings.** If you schedule two tasks (for the same or different pets) at the exact same date and time, `Scheduler.detect_conflicts()` shows a yellow warning banner so you can reschedule.
7. **Complete tasks.** Marking a task complete calls `Pet.complete_task()`; if the task was daily/weekly, the next occurrence is automatically added.

Example workflow: *add a pet → schedule a task → schedule a second task at the same time → see the conflict warning → view the sorted schedule → mark a task complete.*

The CLI demo (`python3 main.py`) shows the same `Scheduler` behavior in the terminal — see the [Sample Output](#-sample-output) above.
