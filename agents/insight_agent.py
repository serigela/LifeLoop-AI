"""
Insight Agent - Aggregates data from all agents and generates holistic insights.
Subscribes to all agent events and produces daily summaries.
"""
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any

from agents.base_agent import BaseAgent
from core.message_bus import MessageBus, Event

logger = logging.getLogger(__name__)


class InsightAgent(BaseAgent):
    """
    Meta-agent that synthesizes insights from all other agents.
    Generates natural language summaries of user's daily patterns.
    """

    def __init__(self, message_bus: MessageBus):
        super().__init__(message_bus, "InsightAgent", processing_interval=600)
        self.event_queue = None
        self.collected_insights: Dict[str, Any] = {
            'activity': None,
            'finance': None,
            'email': None
        }
        self.insight_history: List[Dict] = []

    async def initialize(self):
        """Subscribe to all agent events."""
        logger.info(f"{self.name}: Subscribing to agent events...")

        self.event_queue = self.message_bus.subscribe('*')

        logger.info(f"{self.name}: Subscribed to all events")

    async def _consume_events(self):
        """Continuously consume events from other agents."""
        while self.running:
            try:
                event: Event = await asyncio.wait_for(
                    self.event_queue.get(),
                    timeout=1.0
                )

                logger.info(f"{self.name}: Received {event.event_type} from {event.source_agent}")

                if event.event_type == "activity_summary":
                    self.collected_insights['activity'] = event.data

                elif event.event_type == "finance_insight":
                    self.collected_insights['finance'] = event.data

                elif event.event_type == "email_summary":
                    self.collected_insights['email'] = event.data

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"{self.name}: Error consuming event: {e}")

    def _generate_insight_text(self) -> str:
        """Generate natural language insight from collected data."""
        insights = []

        if self.collected_insights['activity']:
            activity_data = self.collected_insights['activity']
            routines = activity_data.get('routines', {})
            insights.append(
                f"Activity: Detected {len(routines)} routine patterns from "
                f"{activity_data.get('total_activities', 0)} activities."
            )

        if self.collected_insights['finance']:
            finance_data = self.collected_insights['finance'].get('insights', {})
            total_spent = finance_data.get('total_spent', 0)
            anomalies = finance_data.get('anomalies_detected', 0)

            finance_text = f"Finance: Spent ${total_spent:.2f} in last {finance_data.get('analysis_period_days', 0)} days"
            if anomalies > 0:
                finance_text += f" with {anomalies} unusual transaction(s) detected"
            insights.append(finance_text + ".")

        if self.collected_insights['email']:
            email_data = self.collected_insights['email']
            unread = email_data.get('total_unread', 0)
            high_priority = email_data.get('high_priority_count', 0)

            email_text = f"Email: {unread} unread message(s)"
            if high_priority > 0:
                email_text += f", {high_priority} require immediate attention"
            insights.append(email_text + ".")

        if not insights:
            return "Gathering insights from your daily activities..."

        return " | ".join(insights)

    async def process(self):
        """Generate and publish aggregated insights."""
        logger.info(f"{self.name}: Generating holistic insights...")

        insight_text = self._generate_insight_text()

        insight_package = {
            "summary": insight_text,
            "detailed_insights": self.collected_insights.copy(),
            "timestamp": datetime.now().isoformat(),
            "data_freshness": {
                key: value is not None
                for key, value in self.collected_insights.items()
            }
        }

        self.insight_history.append(insight_package)

        if len(self.insight_history) > 100:
            self.insight_history = self.insight_history[-100:]

        logger.info(f"{self.name}: {insight_text}")

        await self.publish_event(
            event_type="daily_insight",
            data=insight_package
        )

        logger.info(f"{self.name}: Published aggregated insights")

    async def run(self):
        """Override run to handle both event consumption and periodic processing."""
        self.running = True
        logger.info(f"{self.name} starting...")

        try:
            await self.initialize()
            logger.info(f"{self.name} initialized successfully")

            event_consumer_task = asyncio.create_task(self._consume_events())

            while self.running:
                try:
                    await self.process()
                    await asyncio.sleep(self.processing_interval)
                except Exception as e:
                    logger.error(f"{self.name} processing error: {e}", exc_info=True)
                    await asyncio.sleep(5)

            event_consumer_task.cancel()
            await asyncio.gather(event_consumer_task, return_exceptions=True)

        except Exception as e:
            logger.error(f"{self.name} failed to initialize: {e}", exc_info=True)
        finally:
            logger.info(f"{self.name} stopped")

    def get_recent_insights(self, limit: int = 10) -> List[Dict]:
        """Return recent insights for dashboard display."""
        return self.insight_history[-limit:]
