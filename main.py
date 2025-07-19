import logging
from src.utils.logger import setup_logging

setup_logging()

main_logger = logging.getLogger(__name__)
main_logger.info("Application starting up ...")

def main():
    pass

if __name__ == "__main__":
    main()