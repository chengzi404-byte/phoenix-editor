from loguru import logger
import os
import time


class NonLogger:
    def info(self, msg):
        pass

    def warn(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass

    def critical(self, msg):
        pass

def setup_logger(log_dir="./logs", debug=False):
    """Setup logger"""
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        if not debug:
            raise TypeError("Non-debug setup, but found setup logger action.")

        log_dir = f"{log_dir}/Logfile-{int(time.time())}.log"

        logger.add(log_dir)

        return logger
    except Exception as e:
        print(f"Failed to setup logger: {e}")
        
        logger = NonLogger()

        return logger