# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Backend classes (current state)

The logic layer lives in `pawpal_system.py` and has four classes:

- **Task** — one care item. Holds `description`, `due_at`, `completed`, `priority`, and `frequency`. Can `mark_complete()` and check `is_due_today()`.
- **Pet** — a single animal with `name`, `species`, `age`, and its own `tasks` list. Can `add_task()`, `list_tasks()`, and `get_incomplete_tasks()`.
- **Owner** — the person using the app. Holds `name`, `email`, and a list of `pets`. Can `add_pet()`, `list_pets()`, and `get_all_tasks()` (which returns `(pet, task)` pairs across every pet).
- **Scheduler** — takes an `Owner` and works across all of that owner's pets. Can `sort_tasks_by_due_time()`, `filter_incomplete_tasks()`, `tasks_due_today()`, and `format_schedule()` for readable output.

## Run the demo

```bash
python main.py
```

This builds a sample owner with two pets and a few tasks, then prints today's schedule sorted by due time.

## Run the Streamlit app

```bash
streamlit run app.py
```

`app.py` is wired to the `pawpal_system.py` logic layer. Adding a pet creates a real `Pet` through `Owner.add_pet()`, scheduling a task creates a real `Task` added to the selected pet, and the schedule section uses `Scheduler` to sort tasks across all pets. Objects are kept in `st.session_state` for the browser session (nothing is saved to disk yet).

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Running `python main.py` shows sorting, filtering, recurring tasks, and conflict detection (times come from "today" so they'll match the day you run it):

```
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
python -m pytest
```

Current coverage: `tests/test_pawpal.py` covers completing a task (`test_mark_complete`), adding a task to a pet (`test_add_task_to_pet`), sorting across pets (`test_scheduler_sorts_by_due_time`), filtering by pet/status (`test_filter_tasks_by_pet_and_status`), recurring task creation (`test_recurring_task_creates_next_occurrence`), and conflict detection (`test_detect_conflicts_on_same_due_time`).

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/austinstanleyhinson/Desktop/AI-110/ai110-module2show-pawpal-starter
collected 6 items

tests/test_pawpal.py ......                                              [100%]

============================== 6 passed in 0.01s ===============================
```

## 📐 Smarter Scheduling

The `Scheduler` works across every pet the owner has (not just one). Each feature maps to a method:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_tasks_by_due_time()` | Returns all `(pet, task)` pairs sorted chronologically by `due_at`. |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)`, `Scheduler.filter_incomplete_tasks()` | Filter by pet name (case-insensitive) and/or completion status. |
| Recurring tasks | `Task.create_next_occurrence()`, `Pet.complete_task()`, `Scheduler.complete_task()` | Completing a `daily`/`weekly` task auto-adds the next occurrence (`once` returns none). |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags tasks that share the exact same `due_at`. Only exact-time matches (no duration field yet). |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
