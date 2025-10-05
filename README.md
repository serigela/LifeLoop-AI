# 🌤️ LifeLoop-AI  
**AI-Powered Personal Automation & Decision Engine**  

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue?logo=python)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Made with ML](https://img.shields.io/badge/Made%20with-Machine%20Learning-orange)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

LifeLoop AI is a **Python-powered personal automation system** that learns your habits and makes smart, explainable decisions about your daily life — from calendar events and spending to emails, workouts, and sleep patterns.  

Using **machine learning**, **LLMs**, and **local orchestration**, LifeLoop helps you understand yourself better and optimize your day automatically.  

---

## 🚀 Features  

### 🧠 Smart Habit Learning  
- Learns your daily routine using clustering and time-series models.  
- Predicts your *optimal* time for meetings, workouts, and breaks.  

### 💸 Expense Categorization & Insights  
- Classifies and visualizes your spending automatically with NLP models.  
- Detects spending anomalies (e.g., “Eating out increased 27% this week”).  

### 📨 Email Summarization & Prioritization  
- Summarizes unread emails with LLMs (OpenAI API or local models).  
- Prioritizes senders based on your historic engagement patterns.  

### 💬 Daily AI Insights  
- Generates natural-language summaries of your behavior:  
  > “You’ve been working late 3 nights this week. Maybe reschedule your 7AM call tomorrow?”  
- Merges insights across all domains — time, finance, and focus.  

### 📊 Unified Dashboard  
- Clean, real-time Python dashboard (Streamlit/Dash) to track habits, tasks, and alerts.  
- Configurable widgets for transactions, schedules, and AI-generated tips.  

---

## 🧩 System Architecture  
lifeloop/
├── core/
│    ├── orchestrator.py         # Central agent scheduler
│    ├── message_bus.py          # Async communication layer
├── agents/
│    ├── activity_agent.py       # Routine and behavior modeling
│    ├── finance_agent.py        # Transaction classification + anomaly detection
│    ├── email_agent.py          # LLM summarization + priority scoring
│    ├── insight_agent.py        # Contextual AI insights + recommendations
├── data/
│    ├── calendar_events.db
│    ├── transactions.csv
│    ├── email_cache/
├── dashboard/
│    └── lifeloop_app.py         # Streamlit dashboard
├── requirements.txt
└── README.md

---

## ⚙️ Tech Stack  

| Category | Tools & Frameworks |
|-----------|--------------------|
| **Core Language** | Python 3.11+ |
| **ML / AI** | PyTorch, scikit-learn, sentence-transformers, LangChain |
| **Data Processing** | pandas, NumPy, SQLite |
| **Automation / Orchestration** | FastAPI, asyncio, Celery |
| **Visualization** | Streamlit / Dash |
| **Optional Enhancements** | MLflow, Redis, Whisper (for voice), FAISS (for memory) |

---

## 🧠 How It Works  

1. **Data Ingestion:** LifeLoop connects to APIs (Google Calendar, Gmail, or local CSVs) to collect context data.  
2. **ML Pipeline:** Agents analyze your routines, transactions, and communication patterns.  
3. **Insight Generation:** A meta-agent aggregates insights and uses an LLM to translate them into readable advice.  
4. **Dashboard:** Real-time visualization keeps you aware and in control.  

---

## 🧪 Example Use Cases  

| Scenario | LifeLoop’s Response |
|-----------|---------------------|
| You’ve had 5 late nights | “Reschedule your 7AM meeting tomorrow.” |
| Coffee spending spikes | “You spent $42 on coffee this week — 60% higher than average.” |
| Inbox overload | “Summarized 12 unread emails. 3 require urgent replies.” |
| Missed workouts | “Your average step count dropped 15%. Want to block a gym slot this weekend?” |

---

## 🛠️ Getting Started

### 1️⃣ Clone the Repo
```bash
git clone https://github.com/<your-username>/LifeLoop-AI.git
cd LifeLoop-AI
```

### 2️⃣ Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment (Optional)
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY if you want LLM-powered email summaries
```

### 5️⃣ Run the Orchestrator
Start all intelligent agents:
```bash
python run.py
```

This will start:
- Activity Agent (analyzes routines and patterns)
- Finance Agent (categorizes expenses and detects anomalies)
- Email Agent (summarizes messages)
- Insight Agent (generates holistic insights)

### 6️⃣ Launch the Dashboard
In a separate terminal, run:
```bash
streamlit run dashboard/lifeloop_app.py
```

The dashboard will open in your browser at `http://localhost:8501`

---

## 🗺️ Roadmap

- ✅ v0.1 — Core Agents (Calendar, Finance, Insights)
- 🔄 v0.2 — Email Agent + Real-Time Updates
- 🚀 v0.3 — Voice Commands & Personalized Scheduling
- 🤖 v1.0 — Fully Autonomous Routine Optimization

## 💡 Future Ideas

- Integrate LangGraph for multi-agent coordination
- Add sleep + activity prediction models using wearable data
- Enable voice-based assistant interface ("What should I do next?")
- Deploy on AWS Lambda + Docker for local/private cloud operation

---

## 🤝 Contributing

Pull requests are welcome! If you'd like to contribute an agent or dataset connector, open an issue or fork the repo.

---

## 📄 License

MIT License — free for personal and commercial use.

---

## 👤 Author

**Srijan Erigela**
- Gmail: Srijanreddye@gmail.com
- LinkedIn: https://www.linkedin.com/in/serigela/
