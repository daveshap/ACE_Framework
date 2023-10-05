import logging
import os

from ace import constants

logging.basicConfig(level=logging.DEBUG)


def get_log_level(level_str):
    level = logging.getLevelName(level_str)
    if not isinstance(level, int):
        raise ValueError(f'Invalid log level: {level_str}')
    return level


# Set the log level for third party loggers separately.
for base_logger in constants.THIRD_PARTY_LOGGERS:
    log_level = os.getenv('ACE_THIRD_PARTY_LOG_LEVEL', constants.THIRD_PARTY_LOG_LEVEL)
    logging.getLogger(base_logger).setLevel(get_log_level(log_level))


class Logger:

    def __new__(cls, name):
        logger = logging.getLogger(name)
        # Prevent duplicate loggers.
        if logger.hasHandlers():
            return logger
        logger.setLevel(logging.DEBUG)
        log_console_handler = logging.StreamHandler()
        log_level = os.getenv('ACE_LOG_LEVEL', constants.LOG_LEVEL)
        log_console_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
        log_console_handler.setLevel(get_log_level(log_level))
        logger.addHandler(log_console_handler)
        if constants.LOG_FILEPATH:
            log_file_handler = logging.FileHandler(constants.LOG_FILEPATH, "a")
            log_file_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
            log_file_handler.setLevel(get_log_level(log_level))
            logger.addHandler(log_file_handler)
        return logger
