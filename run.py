#!/usr/bin/env python3
"""
LifeLoop AI - Main Entry Point
Launches the orchestrator to run all intelligent agents concurrently.
"""
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.orchestrator import Orchestrator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('lifeloop.log')
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point for LifeLoop AI system."""
    logger.info("=" * 60)
    logger.info("LifeLoop AI - Personal Automation System")
    logger.info("=" * 60)
    logger.info("")
    logger.info("Starting orchestrator...")
    logger.info("")
    logger.info("Press Ctrl+C to stop")
    logger.info("")

    orchestrator = Orchestrator()

    try:
        asyncio.run(orchestrator.run())
    except KeyboardInterrupt:
        logger.info("\nShutdown requested by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("LifeLoop AI stopped")


if __name__ == "__main__":
    main()
