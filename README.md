# 🚀 GoalPilot

### AI-Powered Goal Execution Planner

GoalPilot is an AI agent that transforms ambitious goals into structured, actionable execution plans. Instead of wondering *where to start*, users receive a personalized roadmap with weekly milestones, task breakdowns, progress tracking, timeline visualization, and downloadable reports.

Built using **Python, Streamlit, LangChain, and Groq LLMs**, GoalPilot bridges the gap between goal setting and execution.

---

## 🎯 Problem Statement

Many people have goals but struggle with:

- Breaking large goals into manageable steps
- Creating realistic timelines
- Maintaining consistency and accountability
- Tracking progress effectively

GoalPilot solves this by generating AI-driven execution plans tailored to a user's timeline and difficulty level.

---

## ✨ Features

### 🤖 AI-Powered Planning
Generate personalized execution plans using Large Language Models (LLMs).

### 📅 Weekly Roadmaps
Automatically converts goals into structured weekly milestones and actionable tasks.

### 🎚 Difficulty-Based Planning
Plans adapt based on selected difficulty:

- Easy → 2–3 tasks per week
- Medium → 3–5 tasks per week
- Hard → 5–7 tasks per week

### 📊 Progress Tracking
Track completed tasks with interactive checkboxes and monitor overall completion percentage.

### 📆 Timeline Visualization
Visualize your execution roadmap through an interactive Gantt-style timeline.

### 📄 PDF Export
Download generated plans as professional PDF reports.

### 📂 Goal Management
- Save multiple goals
- Pin important goals
- Rename goals
- Delete goals
- Resume progress anytime

### 🧠 Multi-Model Support
Choose between multiple Groq-hosted models:

- Llama 3.1 8B
- Llama 3.3 70B
- Mixtral 8x7B

---

## 🏗️ How It Works

```text
User Goal
    ↓
GoalPilot Agent
    ↓
Prompt Engineering
    ↓
Groq LLM
    ↓
Structured JSON Plan
    ↓
Weekly Tasks & Milestones
    ↓
Progress Tracking & Visualization
```

The AI agent:

1. Accepts a goal, duration, and difficulty level.
2. Uses prompt engineering to generate a structured JSON roadmap.
3. Validates and corrects LLM outputs.
4. Organizes tasks into weekly milestones.
5. Tracks progress across sessions.
6. Visualizes execution timelines.
7. Exports plans as downloadable PDFs.

---

## 🛠️ Tech Stack

| Category | Technology |
|-----------|------------|
| Frontend | Streamlit |
| LLM Framework | LangChain |
| LLM Provider | Groq |
| Models | Llama 3.1, Llama 3.3, Mixtral |
| Data Storage | JSON |
| Visualization | Plotly |
| PDF Generation | ReportLab |
| Language | Python |

---

## 📸 Application Highlights

### Goal Creation
Users enter:
- Goal
- Duration
- Difficulty Level
- Preferred LLM

### AI Plan Generation
GoalPilot generates:
- Weekly tasks
- Milestones
- Execution roadmap

### Progress Dashboard
Track:
- Total Tasks
- Completed Tasks
- Completion Percentage

### Timeline View
Interactive visual representation of the complete execution plan.

---

## 🧠 Agent Design

GoalPilot follows a lightweight AI agent architecture:

### Planner Agent

Responsible for:

- Goal interpretation
- Execution planning
- Weekly milestone generation
- Structured JSON output generation
- Validation and correction of LLM responses

### State Management

Maintains:

- Goal history
- Progress status
- User plans
- Goal metadata

---

## 📂 Project Structure

```text
GoalPilot/
│
├── app.py                # Streamlit application
├── planner.py            # AI planning agent
├── user_data.py          # User data utilities
├── user_data.json        # Goal storage
├── requirements.txt      # Dependencies
└── README.md
```

---
## 📸 Outputs
<img width="1908" height="896" alt="Screenshot 2026-06-01 233528" src="https://github.com/user-attachments/assets/07fc6c64-df12-4f82-8352-e1ba9900d13a" />
<img width="1912" height="884" alt="Screenshot 2026-06-01 233610" src="https://github.com/user-attachments/assets/8aaae83e-4e20-4e72-b5b1-222205994e5f" />
<img width="1895" height="877" alt="Screenshot 2026-06-01 233629" src="https://github.com/user-attachments/assets/99ecc33f-553b-46f6-97df-84a13f596e7d" />

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/GoalPilot.git
cd GoalPilot
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

### Run Application

```bash
streamlit run app.py
```

---

## 🚀 Example Use Cases

### Learning

Goal:
> Learn Data Structures & Algorithms in 3 Months

### Career

Goal:
> Become a Machine Learning Engineer

### Productivity

Goal:
> Build a Consistent Fitness Routine

### Projects

Goal:
> Develop and Deploy an AI Application

---

## 📈 Future Enhancements

- Multi-agent planning system
- Calendar integration
- Email reminders
- Team goal collaboration
- Adaptive plan updates
- RAG-powered recommendations
- Habit tracking analytics
- Cloud database integration

---

## 👩‍💻 Author

**Shanmadi Mohan Nandagopal**

AI & Software Engineering Enthusiast passionate about building intelligent systems that improve productivity and decision-making.

---

## ⭐ Support

If you found this project useful, consider giving it a star ⭐ on GitHub.
