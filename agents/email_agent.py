"""
Email Agent - Summarizes and prioritizes email messages.
Uses LLM to generate intelligent summaries of unread messages.
"""
import logging
import os
from datetime import datetime
from typing import List, Dict

from agents.base_agent import BaseAgent
from core.message_bus import MessageBus

logger = logging.getLogger(__name__)


class EmailAgent(BaseAgent):
    """
    Monitors and summarizes email messages.
    Uses LLM for intelligent email summarization and prioritization.
    """

    def __init__(self, message_bus: MessageBus):
        super().__init__(message_bus, "EmailAgent", processing_interval=240)
        self.mock_emails = []
        self.llm_available = False

    async def initialize(self):
        """Load email data and check LLM availability."""
        logger.info(f"{self.name}: Initializing email processing...")

        self.mock_emails = [
            {
                "id": 1,
                "from": "boss@company.com",
                "subject": "Q4 Budget Review Meeting",
                "body": "Please prepare the Q4 budget analysis for our meeting on Friday. Focus on operational expenses and ROI.",
                "timestamp": datetime.now().isoformat(),
                "priority": "high"
            },
            {
                "id": 2,
                "from": "fitness@gym.com",
                "subject": "Your Weekly Workout Summary",
                "body": "Great work this week! You completed 4 workouts and burned 2,400 calories. Keep it up!",
                "timestamp": datetime.now().isoformat(),
                "priority": "low"
            },
            {
                "id": 3,
                "from": "bank@payments.com",
                "subject": "Payment Due: Credit Card Statement",
                "body": "Your credit card payment of $1,245.67 is due on October 15th. Please ensure sufficient funds.",
                "timestamp": datetime.now().isoformat(),
                "priority": "high"
            },
            {
                "id": 4,
                "from": "newsletter@tech.com",
                "subject": "Latest AI Trends in 2024",
                "body": "Discover the top AI innovations this year including LLMs, multimodal models, and autonomous agents.",
                "timestamp": datetime.now().isoformat(),
                "priority": "medium"
            },
            {
                "id": 5,
                "from": "friend@email.com",
                "subject": "Coffee next week?",
                "body": "Hey! It's been a while. Want to grab coffee and catch up? I'm free Tuesday or Wednesday.",
                "timestamp": datetime.now().isoformat(),
                "priority": "medium"
            }
        ]

        api_key = os.getenv("OPENAI_API_KEY", "")
        self.llm_available = bool(api_key and api_key != "your_openai_api_key_here")

        if not self.llm_available:
            logger.warning(f"{self.name}: OpenAI API key not configured, using rule-based summaries")

        logger.info(f"{self.name}: Loaded {len(self.mock_emails)} emails")

    def _create_rule_based_summary(self, emails: List[Dict]) -> str:
        """Create a summary using rule-based logic when LLM is unavailable."""
        high_priority = [e for e in emails if e['priority'] == 'high']
        medium_priority = [e for e in emails if e['priority'] == 'medium']
        low_priority = [e for e in emails if e['priority'] == 'low']

        summary_parts = [
            f"You have {len(emails)} unread messages.",
        ]

        if high_priority:
            summary_parts.append(
                f"\n🔴 {len(high_priority)} urgent message(s): " +
                ", ".join([f'"{e["subject"]}"' for e in high_priority[:2]])
            )

        if medium_priority:
            summary_parts.append(
                f"\n🟡 {len(medium_priority)} medium priority message(s)"
            )

        if low_priority:
            summary_parts.append(
                f"\n🟢 {len(low_priority)} low priority message(s)"
            )

        return " ".join(summary_parts)

    async def _create_llm_summary(self, emails: List[Dict]) -> str:
        """Create intelligent summary using LLM."""
        try:
            from langchain_openai import ChatOpenAI
            from langchain.schema import HumanMessage

            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

            email_text = "\n\n".join([
                f"From: {e['from']}\nSubject: {e['subject']}\nBody: {e['body']}\nPriority: {e['priority']}"
                for e in emails[:5]
            ])

            prompt = f"""Summarize these emails in 2-3 concise sentences, highlighting the most important items:

{email_text}

Provide a friendly, actionable summary."""

            response = llm.invoke([HumanMessage(content=prompt)])
            return response.content

        except Exception as e:
            logger.error(f"{self.name}: LLM summarization failed: {e}")
            return self._create_rule_based_summary(emails)

    async def process(self):
        """Process and summarize emails."""
        logger.info(f"{self.name}: Processing {len(self.mock_emails)} emails...")

        if self.llm_available:
            summary = await self._create_llm_summary(self.mock_emails)
            logger.info(f"{self.name}: Generated LLM-based summary")
        else:
            summary = self._create_rule_based_summary(self.mock_emails)
            logger.info(f"{self.name}: Generated rule-based summary")

        email_data = {
            "total_unread": len(self.mock_emails),
            "high_priority_count": sum(1 for e in self.mock_emails if e['priority'] == 'high'),
            "summary": summary,
            "top_senders": list(set([e['from'] for e in self.mock_emails[:5]])),
            "analysis_timestamp": datetime.now().isoformat()
        }

        await self.publish_event(
            event_type="email_summary",
            data=email_data
        )

        logger.info(f"{self.name}: Published email summary")
