"""
Main orchestrator for LifeLoop AI system.
Initializes and coordinates all intelligent agents using async task management.
"""
import asyncio
import logging
import signal
from typing import List, Optional
from datetime import datetime

from core.message_bus import MessageBus
from agents.activity_agent import ActivityAgent
from agents.finance_agent import FinanceAgent
from agents.email_agent import EmailAgent
from agents.insight_agent import InsightAgent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Orchestrator:
    """
    Central coordinator for all LifeLoop AI agents.
    Manages agent lifecycle and orchestrates communication.
    """

    def __init__(self):
        self.message_bus = MessageBus()
        self.agents = []
        self.running = False
        self.tasks: List[asyncio.Task] = []
        logger.info("Orchestrator initialized")

    def register_agents(self):
        """Initialize and register all agents."""
        logger.info("Registering agents...")

        self.agents = [
            ActivityAgent(self.message_bus),
            FinanceAgent(self.message_bus),
            EmailAgent(self.message_bus),
            InsightAgent(self.message_bus)
        ]

        logger.info(f"Registered {len(self.agents)} agents")

    async def start_agents(self):
        """Start all agents as concurrent async tasks."""
        logger.info("Starting all agents...")

        for agent in self.agents:
            task = asyncio.create_task(agent.run())
            self.tasks.append(task)
            logger.info(f"Started {agent.__class__.__name__}")

        logger.info("All agents running")

    async def stop_agents(self):
        """Gracefully stop all running agents."""
        logger.info("Stopping all agents...")

        for agent in self.agents:
            await agent.stop()

        for task in self.tasks:
            task.cancel()

        await asyncio.gather(*self.tasks, return_exceptions=True)
        logger.info("All agents stopped")

    async def run(self):
        """Main orchestration loop."""
        self.running = True
        logger.info("=== LifeLoop AI Orchestrator Started ===")
        logger.info(f"System time: {datetime.now()}")

        self.register_agents()
        await self.start_agents()

        try:
            while self.running:
                await asyncio.sleep(1)

                stats = self.message_bus.get_stats()
                if any(task.done() for task in self.tasks):
                    logger.warning("Some agent tasks have stopped unexpectedly")
                    for i, task in enumerate(self.tasks):
                        if task.done():
                            logger.error(f"Agent {self.agents[i].__class__.__name__} stopped")
                            try:
                                await task
                            except Exception as e:
                                logger.error(f"Agent error: {e}")

        except KeyboardInterrupt:
            logger.info("Shutdown signal received")
        finally:
            await self.stop_agents()
            self.running = False
            logger.info("=== LifeLoop AI Orchestrator Stopped ===")

    async def shutdown(self):
        """Signal shutdown to orchestrator."""
        logger.info("Initiating shutdown...")
        self.running = False


async def main():
    """Entry point for orchestrator."""
    orchestrator = Orchestrator()

    loop = asyncio.get_event_loop()

    def signal_handler():
        logger.info("Received shutdown signal")
        asyncio.create_task(orchestrator.shutdown())

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    await orchestrator.run()


if __name__ == "__main__":
    asyncio.run(main())
