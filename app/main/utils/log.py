import logging
from .. import config


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(config.LOGGING_LEVEL)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s : %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
