"""
LifeLoop AI Dashboard - Real-time visualization of agent insights.
Built with Streamlit for interactive data exploration.
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


st.set_page_config(
    page_title="LifeLoop AI Dashboard",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)


def generate_mock_activity_data():
    """Generate mock activity data for visualization."""
    dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq='D')
    activities = ['work', 'exercise', 'social', 'rest']

    data = []
    for date in dates:
        for activity in activities:
            data.append({
                'date': date,
                'activity': activity,
                'hours': np.random.uniform(1, 6)
            })

    return pd.DataFrame(data)


def generate_mock_finance_data():
    """Generate mock financial data for visualization."""
    categories = ['groceries', 'entertainment', 'transport', 'utilities', 'dining', 'shopping']
    spending = {cat: np.random.uniform(50, 500) for cat in categories}
    return spending


def generate_mock_insights():
    """Generate mock insights data."""
    return [
        {
            "timestamp": (datetime.now() - timedelta(hours=i)).strftime("%Y-%m-%d %H:%M"),
            "summary": f"Insight {i+1}: System detected routine patterns and analyzed spending habits.",
            "activity_count": np.random.randint(10, 50),
            "finance_total": np.random.uniform(100, 1000),
            "email_count": np.random.randint(5, 25)
        }
        for i in range(10)
    ]


def main():
    """Main dashboard application."""

    st.title("🔄 LifeLoop AI Dashboard")
    st.markdown("*Your intelligent personal automation system*")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select View",
        ["Overview", "Activity Patterns", "Financial Insights", "Email Summary", "System Status"]
    )

    if page == "Overview":
        render_overview()
    elif page == "Activity Patterns":
        render_activity_patterns()
    elif page == "Financial Insights":
        render_financial_insights()
    elif page == "Email Summary":
        render_email_summary()
    elif page == "System Status":
        render_system_status()


def render_overview():
    """Render overview dashboard."""
    st.header("📊 System Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Active Agents",
            value="4",
            delta="All operational"
        )

    with col2:
        st.metric(
            label="Routines Detected",
            value="12",
            delta="+2 this week"
        )

    with col3:
        st.metric(
            label="Weekly Spending",
            value="$847",
            delta="-15% vs last week"
        )

    with col4:
        st.metric(
            label="Unread Emails",
            value="23",
            delta="5 high priority"
        )

    st.markdown("---")

    st.subheader("📝 Recent Insights")

    insights = generate_mock_insights()

    for insight in insights[:5]:
        with st.expander(f"🔍 {insight['timestamp']}", expanded=False):
            st.write(insight['summary'])
            cols = st.columns(3)
            cols[0].metric("Activities", insight['activity_count'])
            cols[1].metric("Spending", f"${insight['finance_total']:.2f}")
            cols[2].metric("Emails", insight['email_count'])

    st.markdown("---")

    st.subheader("🎯 Quick Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Refresh All Agents", use_container_width=True):
            st.success("Agents refreshed successfully!")

    with col2:
        if st.button("📧 Summarize Emails", use_container_width=True):
            st.info("Email summarization in progress...")

    with col3:
        if st.button("💰 Analyze Spending", use_container_width=True):
            st.info("Financial analysis initiated...")


def render_activity_patterns():
    """Render activity patterns page."""
    st.header("🏃 Activity Patterns")

    activity_df = generate_mock_activity_data()

    st.subheader("Weekly Activity Breakdown")
    pivot_df = activity_df.pivot_table(
        values='hours',
        index='date',
        columns='activity',
        aggfunc='sum'
    )
    st.bar_chart(pivot_df)

    st.markdown("---")

    st.subheader("Activity Summary by Type")
    total_by_activity = activity_df.groupby('activity')['hours'].sum().sort_values(ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(
            total_by_activity.to_frame('Total Hours'),
            use_container_width=True
        )

    with col2:
        activity_pct = (total_by_activity / total_by_activity.sum() * 100).round(1)
        st.write("**Percentage Distribution**")
        for activity, pct in activity_pct.items():
            st.progress(pct / 100, text=f"{activity.capitalize()}: {pct}%")

    st.markdown("---")

    st.subheader("🎯 Detected Routines")

    routines = [
        {"name": "Morning Workout", "confidence": 0.92, "frequency": "Daily", "time": "6:30 AM"},
        {"name": "Work Block", "confidence": 0.88, "frequency": "Weekdays", "time": "9:00 AM"},
        {"name": "Evening Social", "confidence": 0.75, "frequency": "Wed, Fri", "time": "7:00 PM"},
        {"name": "Weekend Rest", "confidence": 0.85, "frequency": "Sat, Sun", "time": "Variable"},
    ]

    for routine in routines:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        col1.write(f"**{routine['name']}**")
        col2.write(routine['frequency'])
        col3.write(routine['time'])
        col4.progress(routine['confidence'], text=f"{routine['confidence']*100:.0f}%")


def render_financial_insights():
    """Render financial insights page."""
    st.header("💰 Financial Insights")

    spending_data = generate_mock_finance_data()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Spending by Category")
        st.bar_chart(pd.Series(spending_data))

    with col2:
        st.subheader("Category Breakdown")
        total_spending = sum(spending_data.values())
        for category, amount in sorted(spending_data.items(), key=lambda x: x[1], reverse=True):
            pct = (amount / total_spending) * 100
            st.write(f"**{category.capitalize()}**: ${amount:.2f} ({pct:.1f}%)")

    st.markdown("---")

    st.subheader("🚨 Anomaly Detection")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Transactions", "156", delta="12 this week")

    with col2:
        st.metric("Average Transaction", "$67.34", delta="+$5.20")

    with col3:
        st.metric("Anomalies Detected", "3", delta="2 resolved")

    st.warning("⚠️ Detected 3 unusual transactions:")
    anomalies = [
        {"date": "2024-10-03", "merchant": "Luxury Store", "amount": "$450.00", "category": "shopping"},
        {"date": "2024-10-04", "merchant": "Fine Dining", "amount": "$280.00", "category": "dining"},
        {"date": "2024-10-05", "merchant": "Electronics Hub", "amount": "$890.00", "category": "shopping"},
    ]

    for anomaly in anomalies:
        st.write(f"- **{anomaly['date']}**: {anomaly['merchant']} - {anomaly['amount']} ({anomaly['category']})")

    st.markdown("---")

    st.subheader("📈 Spending Trends")
    trend_dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    trend_data = pd.DataFrame({
        'date': trend_dates,
        'spending': np.random.uniform(30, 150, len(trend_dates))
    })
    trend_data.set_index('date', inplace=True)
    st.line_chart(trend_data)


def render_email_summary():
    """Render email summary page."""
    st.header("📧 Email Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Unread", "23", delta="-5 today")

    with col2:
        st.metric("High Priority", "5", delta="+2 today")

    with col3:
        st.metric("Newsletters", "12", delta="Auto-filtered")

    st.markdown("---")

    st.subheader("🎯 Priority Inbox")

    priority_emails = [
        {
            "from": "boss@company.com",
            "subject": "Q4 Budget Review Meeting",
            "preview": "Please prepare the Q4 budget analysis...",
            "priority": "🔴 High",
            "time": "2 hours ago"
        },
        {
            "from": "bank@payments.com",
            "subject": "Payment Due: Credit Card Statement",
            "preview": "Your credit card payment of $1,245.67 is due...",
            "priority": "🔴 High",
            "time": "5 hours ago"
        },
        {
            "from": "client@business.com",
            "subject": "Project Deliverable Review",
            "preview": "Can we schedule a call to discuss...",
            "priority": "🟡 Medium",
            "time": "1 day ago"
        },
        {
            "from": "newsletter@tech.com",
            "subject": "Latest AI Trends in 2024",
            "preview": "Discover the top AI innovations...",
            "priority": "🟢 Low",
            "time": "2 days ago"
        },
    ]

    for email in priority_emails:
        with st.expander(f"{email['priority']} | {email['subject']} - {email['time']}", expanded=False):
            st.write(f"**From:** {email['from']}")
            st.write(f"**Preview:** {email['preview']}")
            col1, col2 = st.columns(2)
            with col1:
                st.button("✅ Mark Read", key=f"read_{email['from']}")
            with col2:
                st.button("⭐ Star", key=f"star_{email['from']}")

    st.markdown("---")

    st.subheader("🤖 AI Summary")
    st.info(
        "📝 You have 5 messages requiring immediate attention: "
        "Q4 budget meeting prep and credit card payment due Oct 15th. "
        "3 medium priority messages about project reviews. "
        "12 newsletters have been auto-filtered for later reading."
    )


def render_system_status():
    """Render system status page."""
    st.header("⚙️ System Status")

    st.subheader("🤖 Agent Status")

    agents = [
        {"name": "Activity Agent", "status": "Running", "last_update": "2 min ago", "health": 100},
        {"name": "Finance Agent", "status": "Running", "last_update": "5 min ago", "health": 98},
        {"name": "Email Agent", "status": "Running", "last_update": "3 min ago", "health": 100},
        {"name": "Insight Agent", "status": "Running", "last_update": "1 min ago", "health": 95},
    ]

    for agent in agents:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

        with col1:
            st.write(f"**{agent['name']}**")

        with col2:
            if agent['status'] == "Running":
                st.success(agent['status'])
            else:
                st.error(agent['status'])

        with col3:
            st.write(agent['last_update'])

        with col4:
            st.progress(agent['health'] / 100, text=f"{agent['health']}%")

    st.markdown("---")

    st.subheader("📊 System Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Uptime", "4 days, 12 hours", delta="Stable")

    with col2:
        st.metric("Events Processed", "1,247", delta="+89 today")

    with col3:
        st.metric("Data Points Analyzed", "15.3K", delta="+1.2K today")

    st.markdown("---")

    st.subheader("📡 Message Bus Activity")

    events_data = pd.DataFrame({
        'time': pd.date_range(start=datetime.now() - timedelta(hours=24), end=datetime.now(), freq='H'),
        'events': np.random.randint(10, 100, 25)
    })
    events_data.set_index('time', inplace=True)

    st.line_chart(events_data)

    st.markdown("---")

    st.subheader("🔧 System Configuration")

    config = {
        "Python Version": "3.11.5",
        "Processing Interval": "5 minutes",
        "Data Storage": "SQLite",
        "LLM Provider": "OpenAI GPT-3.5",
        "ML Framework": "scikit-learn + PyTorch"
    }

    for key, value in config.items():
        st.write(f"**{key}:** {value}")


if __name__ == "__main__":
    main()
