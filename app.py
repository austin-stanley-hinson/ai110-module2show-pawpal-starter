"""PawPal+ Streamlit UI.

Connects the Streamlit interface to the backend classes in pawpal_system.py.
Real Owner, Pet, and Task objects are kept in st.session_state for the session.
"""

from datetime import datetime, time as time_cls

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
PawPal+ helps a pet owner plan care tasks across all of their pets.
This app uses the backend classes in `pawpal_system.py` (Owner, Pet, Task, Scheduler).
Data lives in your browser session only — it resets when you close the app.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on things like due time and priority.
"""
    )

# Streamlit reruns this whole script on every interaction, so we only create the
# Owner once and keep it in session_state. Otherwise it would reset on each click.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Demo Owner", email="")

owner = st.session_state.owner

st.divider()

# --- Owner setup ---
st.subheader("Owner")
col_name, col_email = st.columns(2)
with col_name:
    owner.name = st.text_input("Owner name", value=owner.name)
with col_email:
    owner.email = st.text_input("Email", value=owner.email)

st.divider()

# --- Add a pet ---
st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="")
    pet_col1, pet_col2 = st.columns(2)
    with pet_col1:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    with pet_col2:
        age = st.number_input("Age (years)", min_value=0, max_value=40, value=1)
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if pet_name.strip():
        owner.add_pet(Pet(name=pet_name.strip(), species=species, age=int(age)))
        st.success(f"Added {pet_name.strip()} to {owner.name}'s pets.")
    else:
        st.warning("Please enter a pet name.")

st.divider()

# --- Schedule a task ---
st.subheader("Schedule a Task")
pets = owner.list_pets()
if not pets:
    st.info("No pets yet. Add a pet above before scheduling a task.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        pet_names = [pet.name for pet in pets]
        selected_pet_name = st.selectbox("Pet", pet_names)
        description = st.text_input("Task description", value="")
        task_col1, task_col2 = st.columns(2)
        with task_col1:
            due_date = st.date_input("Due date", value=datetime.now().date())
        with task_col2:
            due_time = st.time_input("Due time", value=time_cls(9, 0))
        opt_col1, opt_col2 = st.columns(2)
        with opt_col1:
            priority = st.selectbox("Priority (1 = highest)", [1, 2, 3, 4, 5], index=2)
        with opt_col2:
            frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        if description.strip():
            selected_pet = pets[pet_names.index(selected_pet_name)]
            due_at = datetime.combine(due_date, due_time)
            selected_pet.add_task(
                Task(
                    description=description.strip(),
                    due_at=due_at,
                    priority=int(priority),
                    frequency=frequency,
                )
            )
            st.success(f"Added '{description.strip()}' for {selected_pet.name}.")
        else:
            st.warning("Please enter a task description.")

st.divider()

# --- Current pets ---
st.subheader("Current Pets")
if owner.list_pets():
    st.table(
        [
            {
                "Name": pet.name,
                "Species": pet.species,
                "Age": pet.age,
                "Tasks": len(pet.list_tasks()),
            }
            for pet in owner.list_pets()
        ]
    )
else:
    st.info("No pets added yet.")

st.divider()

# Scheduler reads the current session owner, so it always reflects the latest
# pets and tasks the user has added.
scheduler = Scheduler(owner)

# --- Conflict warnings ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    st.subheader("⚠️ Schedule Conflicts")
    st.caption("These tasks are scheduled at the exact same time — you may want to reschedule one.")
    for warning in conflicts:
        st.warning(warning)
    st.divider()

# --- Schedule across all pets ---
st.subheader("Schedule")
all_pairs = scheduler.get_all_tasks()

if not all_pairs:
    st.info("No tasks scheduled yet. Add a task above.")
else:
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        pet_choice = st.selectbox(
            "Filter by pet", ["All pets"] + [pet.name for pet in owner.list_pets()]
        )
    with filter_col2:
        status_choice = st.selectbox("Filter by status", ["All", "Incomplete", "Complete"])

    pet_name = None if pet_choice == "All pets" else pet_choice
    completed = None
    if status_choice == "Incomplete":
        completed = False
    elif status_choice == "Complete":
        completed = True

    # Filter across all pets, then show in due-time order.
    filtered = scheduler.filter_tasks(pet_name=pet_name, completed=completed)
    filtered = sorted(filtered, key=lambda pair: pair[1].due_at)

    if filtered:
        st.table(
            [
                {
                    "Due": task.due_at.strftime("%a %b %d, %I:%M %p"),
                    "Pet": pet.name,
                    "Task": task.description,
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                    "Status": "Complete" if task.completed else "Incomplete",
                }
                for pet, task in filtered
            ]
        )
    else:
        st.info("No tasks match the current filters.")

    # Let the user mark an incomplete task complete (recurring tasks auto-roll over).
    incomplete_pairs = scheduler.filter_incomplete_tasks()
    if incomplete_pairs:
        with st.form("complete_task_form"):
            labels = [
                f"{pet.name}: {task.description} ({task.due_at.strftime('%b %d %I:%M %p')})"
                for pet, task in incomplete_pairs
            ]
            choice = st.selectbox("Mark a task complete", labels)
            complete_submitted = st.form_submit_button("Mark complete")
        if complete_submitted:
            pet_done, task_to_complete = incomplete_pairs[labels.index(choice)]
            next_task = pet_done.complete_task(task_to_complete)
            if next_task is not None:
                st.success(
                    f"Marked complete. Next {next_task.frequency} occurrence added for "
                    f"{next_task.due_at.strftime('%b %d %I:%M %p')}."
                )
            else:
                st.success("Task marked complete.")
            st.rerun()
