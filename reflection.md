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

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

So far I have three tests in `tests/test_pawpal.py`. One checks that `mark_complete()` actually flips a task's `completed` flag to True, one checks that adding a task to a pet makes the pet's task list grow and that the task is really in there, and one checks that the Scheduler sorts tasks by due time across two different pets. I picked these because they're the basic pieces everything else depends on, if a task can't be completed or a pet can't hold its tasks, nothing above it would work. The sorting test also matters because it's the one spot that proves Scheduler is pulling from multiple pets and not just one. I ran them with `python -m pytest` and all three pass. I haven't tested a lot of edge cases yet since the logic is still pretty small.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
