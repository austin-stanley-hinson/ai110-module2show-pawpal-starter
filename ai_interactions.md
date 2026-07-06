# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

### Optional Extensions: Next Available Slot + JSON Persistence

**Files modified**
- pawpal_system.py
- main.py
- app.py
- tests/test_pawpal.py
- README.md
- ai_interactions.md

**Task requested of the agent**

I asked the agent to add one advanced scheduling feature and one persistence feature. For the scheduling feature, I asked for a simple next-available-slot method that checks fixed time intervals instead of changing the whole task model. For persistence, I asked for custom JSON serialization using `to_dict`/`from_dict` methods instead of adding a new library.

**What did the agent do?**

It added `Scheduler.suggest_next_available_slot(...)` (plus a small `get_occupied_slots` helper), JSON conversion methods for `Task`, `Pet`, and `Owner`, and `save_to_json`/`load_from_json` on `Owner` with a `load_owner_or_default` helper. It wired persistence into `app.py` (load on start, auto-save on add, and Save/Reload buttons), added a next-available-slot section to both `main.py` and the Streamlit UI, added tests, and updated the docs. It also added `data.json`/`demo_data.json` to `.gitignore`.

**What did you have to verify or fix manually?**

I checked that the new algorithm stayed simple and did not introduce task durations or a more complicated calendar model. I also checked that `due_at` was saved as an ISO string and loaded back as a real `datetime` object (the round-trip test covers this). After the changes I ran `python3 main.py` and `python3 -m pytest` to confirm the two extensions worked and didn't break the previous scheduler behavior — all 15 tests passed.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
