import logging
import os


def setup_logger():
    """Setup logger"""
    if not os.path.exists("./logs"):
        os.makedirs("./logs")

    logging.basicConfig(
        filename='./logs/editor.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('Phoenix Editor')
