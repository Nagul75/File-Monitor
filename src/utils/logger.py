import logging

LOG_FILE = "fm_log.txt"   # File to store logs in
LOG_LEVEL = logging.INFO  # Default logging level

def setup_logging():
    """Configure logging for the entire application."""

    logging.basicConfig(
        level=LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE)
        ]
    )

