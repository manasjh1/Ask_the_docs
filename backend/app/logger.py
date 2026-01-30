import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    log_format = (
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    root = logging.getLogger()
    root.setLevel(log_level)

    # Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    root.addHandler(console_handler)

    # File rotation
    os.makedirs("logs", exist_ok=True)
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    file_handler.setFormatter(logging.Formatter(log_format))
    root.addHandler(file_handler)

    # Silence noisy libraries
    noisy = [
        "httpx",
        "urllib3",
        "multipart",
        "sentence_transformers",
        "huggingface_hub",
        "faiss",
        "pdfminer"
    ]

    for lib in noisy:
        logging.getLogger(lib).setLevel(logging.WARNING)
