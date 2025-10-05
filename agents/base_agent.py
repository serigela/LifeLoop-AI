"""
Base agent class for all LifeLoop AI agents.
Provides common functionality for event handling and lifecycle management.
"""
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Optional

from core.message_bus import MessageBus, Event

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all intelligent agents.
    Handles message bus interaction and agent lifecycle.
    """

    def __init__(self, message_bus: MessageBus, name: str, processing_interval: int = 60):
        self.message_bus = message_bus
        self.name = name
        self.processing_interval = processing_interval
        self.running = False
        logger.info(f"{self.name} initialized")

    async def publish_event(self, event_type: str, data: dict):
        """Publish an event to the message bus."""
        event = Event(
            event_type=event_type,
            source_agent=self.name,
            data=data
        )
        await self.message_bus.publish(event)

    @abstractmethod
    async def initialize(self):
        """Initialize agent resources (data loading, model setup, etc.)."""
        pass

    @abstractmethod
    async def process(self):
        """Main processing logic for the agent."""
        pass

    async def run(self):
        """Main agent loop."""
        self.running = True
        logger.info(f"{self.name} starting...")

        try:
            await self.initialize()
            logger.info(f"{self.name} initialized successfully")

            while self.running:
                try:
                    await self.process()
                    await asyncio.sleep(self.processing_interval)
                except Exception as e:
                    logger.error(f"{self.name} processing error: {e}", exc_info=True)
                    await asyncio.sleep(5)

        except Exception as e:
            logger.error(f"{self.name} failed to initialize: {e}", exc_info=True)
        finally:
            logger.info(f"{self.name} stopped")

    async def stop(self):
        """Stop the agent gracefully."""
        logger.info(f"{self.name} stopping...")
        self.running = False
