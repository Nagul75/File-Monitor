import logging
from src.monitor.SHA_hashing import sha256_hash
from src.utils.logger import setup_logging


setup_logging()

main_logger = logging.getLogger(__name__)
main_logger.info("Application starting up ...")

def main():
    file_path = "C:\\Users\\pravi\\OneDrive\\Desktop\\Rasume.docx"
    file_hash = sha256_hash(file_path)
    main_logger.info(f"SHA-256 hash of {file_path}: {file_hash}")

if __name__ == "__main__":
    main()
    main_logger.info("SHA-256 hashing module loaded successfully.")