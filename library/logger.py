from loguru import logger
import os
import time
from logging.handlers import RotatingFileHandler

def setup_logger(log_dir="./logs"):
    """Setup logger"""
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_dir = f"{log_dir}/Logfile-{int(time.time())}.log"

        logger.add(log_dir)

        return logger
    except Exception as e:
        print(f"Failed to setup logger: {e}")
        return None