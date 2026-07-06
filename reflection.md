# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

I started by thinking about what a user actually needs to do in PawPal+. The three main actions I identified were adding pets to an owner profile, adding care tasks for each pet, and viewing or organizing all tasks across every pet in one place. That helped me choose the classes based on the problem instead of just adding random objects.

My initial design used four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`. `Owner` represents the person using the app and stores their name, email, and list of pets. `Pet` represents each animal and stores information like name, species, age, and that pet’s task list. `Task` represents one care responsibility, such as feeding, walking, medication, or grooming, with a description, due time, completion status, priority, and frequency. I made `Scheduler` separate because its job is to organize tasks across pets instead of just storing data. That kept the design cleaner because `Owner` and `Pet` mostly manage their own collections, while `Scheduler` handles sorting, filtering, conflict detection, and other scheduling logic.

**b. Design changes**

The biggest design change was how `Scheduler` interacts with the rest of the system. At first, I thought about having it work with one pet at a time. After looking back at the project requirements, that felt too limited because PawPal+ is supposed to help an owner manage multiple pets. I changed `Scheduler` so it takes an `Owner` and uses `owner.get_all_tasks()` to gather tasks across every pet.

That change made the rest of the project easier. The CLI demo, Streamlit UI, and tests could all rely on the same backend logic instead of duplicating task lists in different places. Later, I updated the final UML in `diagrams/uml_final.mmd` so it matched the actual implementation. The four-class design stayed the same, but the final diagram includes methods added later, such as `Scheduler.filter_tasks`, `Scheduler.detect_conflicts`, `Task.create_next_occurrence`, `Pet.complete_task`, and `Scheduler.suggest_next_available_slot`.

During the UI phase, I also connected `app.py` to the real classes in `pawpal_system.py`. The main issue was that Streamlit reruns the script after every interaction, so creating a new `Owner` normally would reset the app after each button click. I used `st.session_state` to keep the owner object alive during the browser session. After that, adding a pet through the UI called `Owner.add_pet()`, scheduling a task called `Pet.add_task()`, and the schedule display used `Scheduler` instead of placeholder data.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

Before the algorithmic phase, PawPal+ could store pets and tasks, but the logic still felt manual. The scheduler needed to do more than just return a list. I added sorting by due time, filtering by pet name or completion status, recurring task handling, conflict detection, and later a next-available-slot feature.

The main constraint I focused on was time. For a daily care schedule, due time matters most because it decides what should happen first. Priority is stored and displayed on each task, but I did not make it the main sorting rule because a pet owner usually needs to know the order of the day first. Filtering also mattered because once there are multiple pets, the full task list can get crowded.

**b. Tradeoffs**

The main tradeoff is in conflict detection. My `Scheduler.detect_conflicts()` method only flags tasks with the exact same `due_at` date and time. It does not detect overlapping tasks, like a 30-minute walk running into a feeding, because my `Task` class does not store duration.

I considered adding duration-based scheduling, but that would have changed the data model and made the project more complicated than it needed to be. For this version, exact-time conflict detection is a reasonable first step because it catches obvious scheduling problems while keeping the code easy to understand. The same tradeoff applies to `Scheduler.suggest_next_available_slot()`: it checks fixed time intervals and exact occupied times, not full calendar blocks.

---

## 3. AI Collaboration

**a. How you used AI**

I used Cursor mainly for design review, implementation support, algorithm brainstorming, testing ideas, and documentation cleanup. The most helpful prompts were the ones where I gave it a specific role and a specific file, such as asking it to review whether my `Scheduler` design worked across multiple pets or asking it to suggest edge cases for a pet scheduler with sorting and recurring tasks.

Using separate chats for different phases helped a lot. One chat focused on UML and class structure, another on implementation, another on algorithms, another on testing, and another on final polish. That kept the suggestions more focused and made it easier for me to evaluate whether each answer matched the current phase.

**b. Judgment and verification**

One AI suggestion I did not accept as-is was duration-based conflict detection. The AI suggested a more advanced time-blocking approach that could check whether two tasks overlap. I rejected that because my `Task` class does not have a duration field, so implementing that suggestion would have forced me to redesign the model just for one feature. I kept the simpler exact-time conflict check and documented it as a tradeoff.

I also avoided adding extra classes like a separate `TaskList` or `Schedule` class. Those might make sense in a larger app, but for this assignment the four-class structure was clearer and matched the rubric better. The AI could generate options quickly, but I still had to decide what fit the design.

I verified AI-generated or AI-assisted changes by running the project instead of just trusting the code. `python3 main.py` showed the end-to-end demo, and `python3 -m pytest` checked the important behaviors directly. I also checked that method names stayed consistent across `pawpal_system.py`, `main.py`, `app.py`, and the test file.

---

## 4. Testing and Verification

**a. What you tested**

I tested the basic object behavior first, then added tests for the smarter scheduling features. The test suite checks that `Task.mark_complete()` changes the completion status, `Pet.add_task()` adds a task to a pet, and `Scheduler.sort_tasks_by_due_time()` returns tasks in chronological order across multiple pets.

After adding the algorithmic layer, I expanded the tests to cover recurrence and conflict detection. The recurrence tests check that completing a daily task creates a new task for the following day, while a one-time task does not create another copy. The conflict tests check that duplicate task times are flagged and distinct times are not. I also included edge cases like an owner with no pets so scheduler methods do not crash when there is no data.

For the optional extensions, I added tests for `Scheduler.suggest_next_available_slot()` and JSON persistence. The persistence test uses a temporary file to save an owner with pets and tasks, load it back, and confirm that important fields like owner name, pet count, task description, and `due_at` still match.

**b. Confidence**

I would rate my confidence around 4 out of 5 stars. The core object interactions and main scheduling features are covered by automated tests, and the CLI demo shows the workflow from creating pets to organizing tasks. I am not giving it 5 stars because this is still a small project with simple assumptions. The app does not handle every messy real-world input, and conflict detection is still based on exact matching times instead of full overlapping time ranges.

If I had more time, I would test more UI edge cases, such as empty task descriptions, tasks scheduled in the past, and duplicate task descriptions for the same pet. I would also test weekly recurrence more thoroughly and make task completion use a more reliable identifier than description matching.

---

## 5. Reflection

**a. What went well**

The part I am most satisfied with is the `Scheduler`. Keeping it separate from `Owner` and `Pet` made the system easier to extend. Since `Scheduler` works through `owner.get_all_tasks()`, it naturally handles multiple pets without needing duplicate logic in the CLI, UI, or tests.

I also liked that the same backend logic works in different places. `main.py` demonstrates the system in the terminal, `app.py` uses it in the Streamlit interface, and the pytest suite verifies the methods directly. That made the project feel more like one connected system instead of separate files doing unrelated things.

**b. What you would improve**

If I had another iteration, I would improve the task model by adding a duration field. That would make conflict detection more realistic because the scheduler could check whether tasks overlap instead of only checking exact matching start times. I would also give each task a unique ID so completing a task does not depend on matching a description.

For stretch work, I added two optional extensions. First, I added `Scheduler.suggest_next_available_slot()` as an advanced algorithmic feature. I chose it because it builds naturally on conflict detection: the scheduler looks at occupied times and returns the first open fixed interval. The tradeoff is that it still uses exact slots instead of full calendar durations.

Second, I added JSON persistence. `Task`, `Pet`, and `Owner` now have custom `to_dict` and `from_dict` methods, and `Owner` has `save_to_json` and `load_from_json`. I chose custom conversion instead of a library like marshmallow because it was easier to understand and avoided adding another dependency. The persistence is still simple because it saves to a local `data.json` file instead of a database, but it is enough for the app to remember pets and tasks between runs.

**c. Key takeaway**

The biggest thing I learned is that having a clear design first makes the rest of the project easier. Once I knew what each class owned, adding the UI, algorithms, tests, and persistence was mostly about extending the same structure instead of starting over.

I also learned that working with AI does not mean letting it make every design decision. Cursor was useful for generating code, suggesting edge cases, and helping compare approaches, but I still had to act as the lead architect. My job was to keep the project consistent, reject suggestions that made the design too complicated, and verify the final behavior with real runs and tests.
