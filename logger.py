import logging
import sys
from datetime import datetime
import os

def setup_logger():
    logger=logging.getLogger("support agent")
    logger.setLevel(logging.DEBUG)

    formatter=logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    os.makedirs("logs", exist_ok=True)
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()