import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from ics import Calendar, Event

from planner import generate_plan

import json
import os

# User data logs
DATA_FILE = "user_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Download
def generate_pdf(plan, start_date):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph(f"Goal: {plan['goal']}", styles["Title"]))
    content.append(Paragraph(f"Duration: {plan['duration_months']} Months", styles["Normal"]))
    content.append(Paragraph(f"Difficulty: {plan['difficulty']}", styles["Normal"]))
    content.append(Paragraph(f"Start Date: {start_date}", styles["Normal"]))

    for milestone in plan["milestones"]:
        content.append(Paragraph(f"<br/><b>{milestone['title']}</b>", styles["Heading2"]))

        for week in milestone["weeks"]:
            content.append(Paragraph(f"Week {week['week']}", styles["Heading3"]))
            for task in week["tasks"]:
                content.append(Paragraph(f"- {task}", styles["Normal"]))

    doc.build(content)
    buffer.seek(0)
    return buffer

#calendar
def generate_calendar(plan, start_date):

    calendar = Calendar()

    current_date = start_date

    for milestone in plan["milestones"]:

        for week in milestone["weeks"]:

            for task in week["tasks"]:

                event = Event()

                event.name = task

                event.begin = current_date.strftime("%Y-%m-%d")

                event.description = (
                    f"Goal: {plan['goal']}\n"
                    f"Milestone: {milestone['title']}\n"
                    f"Week: {week['week']}"
                )

                calendar.events.add(event)

            current_date += datetime.timedelta(days=7)

    return str(calendar)

st.set_page_config(page_title="GoalPilot", layout="wide")

# Session State
if "data" not in st.session_state:
    st.session_state.data = load_data()

if "current_goal" not in st.session_state:
    st.session_state.current_goal = None

st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }

    h1, h2, h3 {
        color: #ffffff;
    }

    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
    }

    .stProgress > div > div > div > div {
        background-color: #00c2ff;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
# 🚀 GoalPilot  
### AI Execution Planner
""")

# User Inputs
st.sidebar.title("🚀 GoalPilot")
st.sidebar.markdown("### Create Your Plan")

goal = st.sidebar.text_area("Enter your goal:")

duration = st.sidebar.selectbox(
    "Select duration (months):",
    [1, 2, 3, 4, 5, 6]
)

difficulty = st.sidebar.selectbox(
    "Select Difficulty Level",
    ["Easy", "Medium", "Hard"]
)

model_name = st.sidebar.selectbox(
    "Choose AI Model",
    [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "mixtral-8x7b-32768"
    ]
)

start_date = st.sidebar.date_input(
    "📅 Select start date:",
    datetime.date.today()
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🧠 Active Goal")
if st.session_state.current_goal:
    active = st.session_state.data.get(st.session_state.current_goal, {})
    st.sidebar.success(active.get("display_name", st.session_state.current_goal))
else:
    st.sidebar.info("No goal selected")

st.sidebar.subheader("📂 Your Goals")

# Sort pinned goals first
goals = st.session_state.data
sorted_goals = sorted(
    goals.items(),
    key=lambda x: x[1].get("pinned", False),
    reverse=True
)

for goal_key, goal_data in sorted_goals:

    display_name = goal_data.get("display_name", goal_key)
    is_pinned = goal_data.get("pinned", False)

    col1, col2, col3, col4 = st.sidebar.columns([3, 1, 1, 1])

    # 👉 Select Goal
    if goal_key == st.session_state.current_goal:
        col1.markdown(f"👉 **{display_name}**")
    else:
        if col1.button(display_name, key=f"select_{goal_key}"):
            st.session_state.current_goal = goal_key

    # ⭐ Pin / Unpin
    if col2.button("⭐" if not is_pinned else "🌟", key=f"pin_{goal_key}"):
        st.session_state.data[goal_key]["pinned"] = not is_pinned
        save_data(st.session_state.data)
        st.rerun()

    # ✏ Rename
    if col3.button("✏", key=f"rename_{goal_key}"):
        st.session_state[f"rename_mode_{goal_key}"] = True

    # ❌ Delete
    if col4.button("❌", key=f"delete_{goal_key}"):
        del st.session_state.data[goal_key]
        save_data(st.session_state.data)

        if st.session_state.current_goal == goal_key:
            st.session_state.current_goal = None

        st.rerun()

    # Rename input
    if st.session_state.get(f"rename_mode_{goal_key}", False):
        new_name = st.sidebar.text_input(
            "New name",
            value=display_name,
            key=f"input_{goal_key}"
        )

        if st.sidebar.button("Save", key=f"save_{goal_key}"):
            st.session_state.data[goal_key]["display_name"] = new_name
            save_data(st.session_state.data)

            st.session_state[f"rename_mode_{goal_key}"] = False
            st.rerun()

generate_clicked = st.sidebar.button("🚀 Generate Plan")

# Generate Plan
if generate_clicked:
    if goal:
        with st.spinner("Generating plan..."):

            plan = generate_plan(goal, duration, difficulty, model_name)

            # Save goal
            goal_key = goal.strip().lower()

            st.session_state.data[goal_key] = {
                "display_name": goal.strip(),
                "plan": plan,
                "progress": {},
                "pinned": False
            }

            save_data(st.session_state.data)

            st.session_state.current_goal = goal_key

            save_data(st.session_state.data)

            # Set active goal
            st.session_state.current_goal = goal_key

    else:
        st.warning("Please enter a goal.")

# LOAD CURRENT PLAN
plan = None

if st.session_state.current_goal:
    goal_data = st.session_state.data.get(st.session_state.current_goal, {})
    plan = goal_data.get("plan")

# Display Plan
if plan:

    if "error" in plan:
        st.error(plan["error"])

    else:

        st.header(f"🎯 Goal: {plan['goal']}")
        st.subheader(f"⏳ Duration: {plan['duration_months']} Months")
        st.subheader(f"⚡ Difficulty: {plan['difficulty']}")
        st.subheader(
            f"📅 Start Date: {start_date.strftime('%B %d, %Y')}"
        )

        total_tasks = 0
        completed_tasks = 0

        current_date = start_date
        calendar_data = []

        for milestone_index, milestone in enumerate(plan["milestones"]):

            st.markdown("---")
            st.subheader(f"📌 {milestone['title']}")

            for week in milestone["weeks"]:

                week_start = current_date
                week_end = week_start + datetime.timedelta(days=6)

                calendar_data.append({
                    "Week": week["week"],
                    "Milestone": milestone["title"],
                    "Start": week_start,
                    "End": week_end
                })

                with st.expander(
                    f"🗓 Week {week['week']} "
                    f"({week_start.strftime('%b %d')} – {week_end.strftime('%b %d')})"
                ):

                    for task_index, task in enumerate(week["tasks"]):

                        task_id = f"{st.session_state.current_goal}_{milestone_index}_{week['week']}_{task_index}"
                        goal_data = st.session_state.data[st.session_state.current_goal]
                        progress_data = goal_data.get("progress", {})
                        checked = st.checkbox(
                            task,
                            key=task_id,
                            value=progress_data.get(task_id, False)
                        )

                        st.session_state.data[st.session_state.current_goal]["progress"][task_id] = checked
                        save_data(st.session_state.data)

                        total_tasks += 1

                        if checked:
                            completed_tasks += 1

                current_date += datetime.timedelta(days=7)

        # Progress
        if total_tasks > 0:

            progress_ratio = completed_tasks / total_tasks

            st.markdown("## 📊 Overall Progress")

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Tasks", total_tasks)
            col2.metric("Completed", completed_tasks)
            col3.metric("Progress %", f"{int(progress_ratio * 100)}%")

            st.progress(progress_ratio)

        # Timeline
        st.markdown("## 📆 Timeline Visualization")

        df = pd.DataFrame(calendar_data)

        fig = px.timeline(
            df,
            x_start="Start",
            x_end="End",
            y="Milestone",
            color="Milestone"
        )

        fig.update_yaxes(autorange="reversed")

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("## 📥 Download Plan")

        downloadable_text = f"Goal: {plan['goal']}\n"
        downloadable_text += f"Duration: {plan['duration_months']} Months\n"
        downloadable_text += f"Difficulty: {plan['difficulty']}\n"
        downloadable_text += f"Start Date: {start_date}\n\n"

        current_date = start_date

        for milestone in plan["milestones"]:

            downloadable_text += f"\n=== {milestone['title']} ===\n"

            for week in milestone["weeks"]:

                week_start = current_date
                week_end = week_start + datetime.timedelta(days=6)

                downloadable_text += (
                    f"\nWeek {week['week']} "
                    f"({week_start} - {week_end})\n"
                )

                for task in week["tasks"]:
                    downloadable_text += f"- {task}\n"

                current_date += datetime.timedelta(days=7)

        pdf = generate_pdf(plan, start_date)

        st.download_button(
            label="📄 Download Plan as PDF",
            data=pdf,
            file_name="GoalPilot_Plan.pdf",
            mime="application/pdf"
        )

        calendar_file = generate_calendar(
        plan,
        start_date
        )

        st.download_button(
            label="📅 Export to Calendar (.ics)",
            data=calendar_file,
            file_name="GoalPilot_Calendar.ics",
            mime="text/calendar"
        )
