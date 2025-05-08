import logging
import os


def setup_logger():
    """设置日志记录器"""
    if not os.path.exists("./logs"):
        os.makedirs("./logs")

    logging.basicConfig(
        filename='./logs/editor.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('Phoenix Editor')
