"""
Message Bus for inter-agent communication using asyncio queues.
Allows agents to publish events and subscribe to specific event types.
"""
import asyncio
import logging
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Event:
    """Event structure for message passing between agents."""
    event_type: str
    source_agent: str
    data: Dict[str, Any]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class MessageBus:
    """
    Asynchronous message bus for agent communication.
    Supports publish-subscribe pattern with event filtering.
    """

    def __init__(self, max_queue_size: int = 1000):
        self.subscribers: Dict[str, List[asyncio.Queue]] = {}
        self.max_queue_size = max_queue_size
        logger.info("MessageBus initialized")

    def subscribe(self, event_type: str) -> asyncio.Queue:
        """
        Subscribe to a specific event type.
        Returns a queue that will receive matching events.
        """
        queue = asyncio.Queue(maxsize=self.max_queue_size)

        if event_type not in self.subscribers:
            self.subscribers[event_type] = []

        self.subscribers[event_type].append(queue)
        logger.info(f"New subscription to event_type: {event_type}")
        return queue

    async def publish(self, event: Event):
        """
        Publish an event to all subscribers of that event type.
        Also publishes to wildcard '*' subscribers.
        """
        logger.info(f"Publishing event: {event.event_type} from {event.source_agent}")

        targets = []
        if event.event_type in self.subscribers:
            targets.extend(self.subscribers[event.event_type])

        if '*' in self.subscribers:
            targets.extend(self.subscribers['*'])

        for queue in targets:
            try:
                await asyncio.wait_for(
                    queue.put(event),
                    timeout=5.0
                )
            except asyncio.TimeoutError:
                logger.warning(f"Queue full, dropping event: {event.event_type}")
            except Exception as e:
                logger.error(f"Error publishing event: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Return current message bus statistics."""
        return {
            "event_types": list(self.subscribers.keys()),
            "subscriber_counts": {
                event_type: len(queues)
                for event_type, queues in self.subscribers.items()
            }
        }
