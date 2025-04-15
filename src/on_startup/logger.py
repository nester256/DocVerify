import logging.config

from src.integrations.logger import LOGGING_CONFIG, logger


def setup_logger() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
    logger.setLevel(logging.DEBUG)
