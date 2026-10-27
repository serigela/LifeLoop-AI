# LifeLoop AI

A local, multi-agent personal analytics demo. Activity, finance, and email agents publish events to an async message bus. An insight agent combines those events into one summary. The dashboard displays the same analysis alongside the underlying sample records.

## What works today

- Activity clustering with scikit-learn over `data/calendar_events.csv`.
- Thirty-day spending totals, category breakdown, and simple amount anomaly detection over `data/transactions.csv`.
- Rule-based summaries of five example emails, with optional OpenAI summarization when configured.
- One-shot JSON demo, continuous async orchestrator, and Streamlit dashboard.
- Unit tests covering sample loading and all three domains in the combined insight.

The calendar and transaction CSVs are synthetic. Their dates are shifted together so the newest row is today; the original spacing and values stay intact. Email records are examples in code. The project does not connect to a live inbox, calendar, or bank account. Spending categories come from the CSV; the demo classifier is trained on those labels but is not used to generate the spending report. Anomaly flags are descriptive and are not financial advice.

## Quick start

Use Python 3.11 or 3.12:

```bash
git clone https://github.com/serigela/LifeLoop-AI.git
cd LifeLoop-AI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py --once
python -m unittest discover -s tests -v
streamlit run dashboard/lifeloop_app.py
```

`python run.py` starts the long-running agents and writes `lifeloop.log`; stop it with Ctrl+C. The dashboard can run independently. `--once` prints complete JSON without leaving a background process.

For optional LLM summaries, install `requirements-llm.txt` and set `OPENAI_API_KEY`. The default demo needs no key or external service.

## Architecture

`core/message_bus.py` publishes typed events to subscriber queues. `core/orchestrator.py` starts the four agents or executes one complete cycle. `core/sample_data.py` loads and re-dates the bundled CSVs. `agents/insight_agent.py` consumes events and creates the combined summary. `dashboard/lifeloop_app.py` renders that result with sample data for inspection.

## Next steps

Add real data connectors with explicit user authorization, durable event storage, a supervised category classifier evaluated on held-out merchant records, and user-specific anomaly baselines. These are planned features, not current capabilities.

MIT licensed.
