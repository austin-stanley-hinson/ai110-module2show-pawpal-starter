# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I started by thinking about what the user actually needs to do in PawPal+. I came up with three core actions: (1) add pets to an owner profile, (2) add care tasks for each pet, and (3) view and organize all the tasks across every pet in one place. That helped me pick my classes instead of just guessing.

I ended up with four: Owner, Pet, Task, and Scheduler. I chose Owner because there's one person the whole app belongs to, and they need to hold their pets and email/name info. Pet made sense because each animal is its own thing with a name, species, age, and its own list of tasks. Task felt obvious since a walk or a feeding is really its own item with a description, a due time, a completed flag, and a priority. I made Scheduler separate on purpose so the "figure out what needs doing" logic doesn't get crammed into Owner or Pet. Owner and Pet mostly just store data and hand back their lists, and Scheduler is the piece that actually sorts, filters, and pulls out what's due today.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

The biggest change was with Scheduler. At first I had it working off a single Pet, like you'd point it at one animal and get that pet's schedule. But once I re-read the scenario, an owner can have more than one pet, and it would be annoying to build a separate schedule per pet. So I changed Scheduler to take the Owner instead, and now it looks at every pet the owner has and gathers all their tasks together. That's why Owner also got a get_all_tasks method, so the Scheduler has an easy way to reach across pets.

Update after Phase 2: I moved from the design into working code, so the UML skeleton is now real classes with actual method bodies instead of `pass`. The main thing I had to check was that Scheduler was not only looking at one pet, since the project expects it to organize tasks across multiple pets. I kept it working through the Owner, so Scheduler calls `owner.get_all_tasks()` and gets tasks from every pet at once. I built a small CLI demo in `main.py` and ran it before doing anything else, because it was easier to see from the terminal whether the objects were actually working together. I also added a couple of pytest tests for simple behavior like completing a task and adding a task to a pet. No Streamlit or saving to a file yet, that's for later.

Update after the polish phase: I made a final UML in `diagrams/uml_final.mmd` and compared it to the code. It's close to my original draft, the four classes and their relationships didn't change, but I added the methods that showed up later like `Scheduler.filter_tasks`, `Scheduler.detect_conflicts`, `Task.create_next_occurrence`, and `Pet.complete_task`, and I updated `Task.priority` to an int. So the final diagram matches what I actually built instead of just the early plan. I also polished the Streamlit UI so it visibly uses the scheduler (sorted table, filter controls, and a conflict warning banner) instead of just storing tasks.

Update after Phase 3: In this phase I connected the Streamlit interface in `app.py` to the classes from `pawpal_system.py`. The main issue was remembering that Streamlit reruns the whole script whenever a button is clicked, so at first the Owner kept getting recreated as an empty object and my pets would disappear. I fixed that by storing the Owner in `st.session_state` and only creating it if it isn't already there. Once the owner was stored there, adding a pet through the UI actually calls `Owner.add_pet()` with a real `Pet`, and scheduling a task creates a real `Task` and calls `Pet.add_task()` on the pet the user picked. The schedule section builds a `Scheduler` from the session owner each run so it always reads the current pets and tasks, and I show it as a table instead of raw objects. I also wired the "mark complete" option to `Task.mark_complete()`. This only lasts for the browser session though, nothing is saved once the app closes since I haven't added file saving.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Up until this phase the logic felt kind of manual. I could add tasks and they'd get stored, but the app didn't really do much to organize them, it was basically just a list. In this phase I made the scheduler more useful. It now sorts tasks by due time so the schedule shows up in time order, it can filter tasks by pet name or by whether they're done, it handles recurring daily/weekly tasks, and it does a lightweight check for tasks scheduled at the exact same time. The main constraint I focused on is due time since that's what actually decides the order of someone's day. Priority is stored on each task and shown in the output, but I'm not sorting by it yet, I decided time mattered most for a daily plan.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The main tradeoff is in how I detect conflicts. My `detect_conflicts()` only flags tasks that have the exact same `due_at` date and time. It does not check for tasks that overlap, like a 30-minute walk running into a feeding, because my Task class doesn't have a duration field. Adding real overlap checking would mean changing the data model to store how long each task takes, and that felt like more than this phase needs. So I kept the exact-time check on purpose to stay simple and match the assignment instead of trying to handle every real scheduling case.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

For the scheduling phase I used AI mostly to brainstorm lightweight scheduling algorithms, since I wasn't sure how complicated conflict detection needed to be. It suggested a few options including a time-blocking approach that checks for overlapping time ranges. I didn't go with that one because my Task class doesn't store a duration, so overlap checking would've forced me to redesign the data model. I kept the simpler exact-time conflict check instead, which fits what I actually have. To make sure the new behavior worked I updated `main.py` to actually show the sorting, filtering, recurring task, and conflict output, and I added pytest tests for the new scheduler methods so I wasn't just trusting the printout.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The clearest example was conflict detection. The AI suggested a duration-based / time-blocking approach that checks whether two tasks overlap in time. I didn't take it because my `Task` class doesn't store a duration, so I'd have had to redesign the data model just to support one feature. I went with the simpler exact-time check instead and wrote it down as a known tradeoff. It also suggested adding a few extra classes (like a separate TaskList or Schedule class), but I kept the four-class structure since the rubric cares about a clear OOP design and the extra classes didn't earn their keep. For the UI it leaned toward a more feature-heavy layout, and I kept mine focused on the core scheduler behavior so it stays readable. I verified suggestions by actually running them: `python3 main.py` shows the end-to-end behavior, and the pytest suite checks the specific methods, so I wasn't trusting code just because it looked plausible.

Working across separate chat sessions for design, implementation, algorithms, testing, and this polish phase actually helped me stay organized, each session had one clear job instead of everything at once. The main thing I learned about being the lead architect is that the AI is good at producing options fast, but I'm the one who has to keep the project consistent (same method names across `app.py`, `main.py`, and the tests) and say no when a suggestion adds complexity the assignment doesn't need.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

So far I have three tests in `tests/test_pawpal.py`. One checks that `mark_complete()` actually flips a task's `completed` flag to True, one checks that adding a task to a pet makes the pet's task list grow and that the task is really in there, and one checks that the Scheduler sorts tasks by due time across two different pets. I picked these because they're the basic pieces everything else depends on, if a task can't be completed or a pet can't hold its tasks, nothing above it would work. The sorting test also matters because it's the one spot that proves Scheduler is pulling from multiple pets and not just one. I ran them with `python -m pytest` and all three pass. I haven't tested a lot of edge cases yet since the logic is still pretty small.

Testing phase update: I focused on making sure the smarter scheduling logic actually worked instead of just looking right in the `main.py` demo. I grew the suite to 11 tests. The most important ones are sorting, recurrence, and conflict detection, since those are the parts most likely to break if I change the scheduler later. I also added a few edge cases: a `once` task shouldn't recur, an owner with no pets shouldn't crash any scheduler method, and distinct times should return no conflicts. AI helped me come up with edge cases I hadn't thought of, but I still had to line the tests up with my actual method names (`Pet.complete_task`, `Scheduler.complete_task`, `create_next_occurrence`, `detect_conflicts`) so they were checking real behavior and not made-up assumptions. When something didn't pass at first I had to stop and figure out whether the test was wrong or the code was wrong, and it was usually my test assuming the wrong return shape.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm fairly confident, around 4 out of 5. The core object interactions and the scheduling algorithms all have tests and they pass, so I trust the main paths. I'm not fully confident because everything is in-memory and I haven't tested messy real-world input yet. If I had more time I'd test weird inputs from the UI (empty descriptions, tasks in the past), weekly recurrence specifically, and what happens when the same task description is used twice for one pet, since `Scheduler.complete_task` matches on description.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most happy with how the Scheduler turned out. Keeping it separate from Owner and Pet and having it work through `owner.get_all_tasks()` meant it naturally handles multiple pets, and adding sorting, filtering, recurring tasks, and conflict detection on top of that felt clean instead of hacky. It was also satisfying to see the same logic show up both in the CLI demo and the Streamlit UI without changing the backend.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

The obvious next step is persistence, right now everything lives in the browser session and disappears when the app closes, so I'd add saving/loading (probably JSON) so a pet owner's data sticks around. I'd also give `Task` a duration field so conflict detection could check real overlaps instead of only exact-time matches, and I'd make `Scheduler.complete_task` match on something more reliable than the task description since two tasks could share a name.

**Optional extensions (stretch work):** I ended up doing two of these as stretch features. First I added a "next available slot" algorithm (`Scheduler.suggest_next_available_slot`) because it builds directly on the conflict-detection idea, it just walks fixed 30-minute slots and returns the first time no task is using. The tradeoff is the same as conflict detection: it only checks fixed intervals and exact `due_at` matches, not real calendar durations, since `Task` still has no duration field. Second I added JSON persistence with custom `to_dict`/`from_dict` methods on Task, Pet, and Owner plus `save_to_json`/`load_from_json`. I chose custom conversion instead of adding a serialization library because it was easier to understand and didn't add a dependency. It's still just a local `data.json` file, not a database, so it's simple persistence rather than anything robust. AI helped scaffold the conversion methods, but I checked the datetime serialization myself (saving as ISO strings and loading back into real `datetime` objects) and added a round-trip test to prove it.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The biggest thing I learned is that starting from the design (UML and the four classes) made everything after it easier. Because I knew what each class owned, connecting the UI, adding algorithms, and writing tests were mostly about filling in clear pieces instead of guessing. And working with AI, I learned it's fastest when I already know the shape I want, so I can accept the parts that fit and reject the parts that would over-complicate it.
