import os
import logging

def configure_logging():
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        logging.basicConfig(
            level=getattr(logging, level, logging.INFO),
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        )
