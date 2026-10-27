"""Local dashboard for the bundled synthetic LifeLoop demo."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from core.orchestrator import Orchestrator
from core.sample_data import load_activities, load_transactions


st.set_page_config(page_title="LifeLoop AI demo", layout="wide")
st.title("LifeLoop AI")
st.caption("Synthetic CSV and example email data. Dates are shifted to the current day for the demo.")


@st.cache_data(ttl=300)
def snapshot():
    return asyncio.run(Orchestrator().run_once())


if st.button("Refresh analysis"):
    snapshot.clear()

result = snapshot()
finance = result["detailed_insights"]["finance"]["insights"]
activity = result["detailed_insights"]["activity"]
email = result["detailed_insights"]["email"]

first, second, third, fourth = st.columns(4)
first.metric("30-day sample spending", f"${finance['total_spent']:,.2f}")
second.metric("Sample transactions", finance["transaction_count"])
third.metric("Activity records", activity["total_activities"])
fourth.metric("Example urgent emails", email["high_priority_count"])

st.subheader("Daily summary")
st.write(result["summary"])

left, right = st.columns(2)
with left:
    st.subheader("Spending by category")
    st.bar_chart(finance["category_breakdown"])
    st.caption("Anomalies are amounts above the sample mean plus two standard deviations.")
    st.dataframe(load_transactions()[["timestamp", "merchant", "amount", "category"]],
                 use_container_width=True, hide_index=True)
with right:
    st.subheader("Activity routines")
    st.dataframe(load_activities()[["timestamp", "activity_type", "duration_minutes", "location"]],
                 use_container_width=True, hide_index=True)
    st.write(email["summary"])
