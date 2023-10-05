import logging
import os

from ace import constants

logging.basicConfig(level=logging.DEBUG)


class ConsoleHandler(logging.StreamHandler):
    pass


class FileLogHandler(logging.FileHandler):
    pass


def get_log_level(level_str):
    level = logging.getLevelName(level_str)
    if not isinstance(level, int):
        raise ValueError(f'Invalid log level: {level_str}')
    return level


# Set the log level for third party loggers separately.
for base_logger in constants.THIRD_PARTY_LOGGERS:
    # Docker Compose sets this to an empty string, so a 'falsy' check is needed here.
    log_level = os.getenv('ACE_THIRD_PARTY_LOG_LEVEL') or constants.THIRD_PARTY_LOG_LEVEL
    logging.getLogger(base_logger).setLevel(get_log_level(log_level))


class Logger:

    def __new__(cls, name):
        logger = logging.getLogger(name)
        log_level = os.getenv('ACE_LOG_LEVEL') or constants.LOG_LEVEL
        logger.setLevel(get_log_level(log_level))
        if not any(isinstance(handler, ConsoleHandler) for handler in logger.handlers):
            log_console_handler = ConsoleHandler()
            log_console_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
            log_console_handler.setLevel(get_log_level(log_level))
            logger.addHandler(log_console_handler)
        if constants.LOG_FILEPATH and not any(isinstance(handler, FileLogHandler) for handler in logger.handlers):
            log_file_handler = FileLogHandler(constants.LOG_FILEPATH, "a")
            log_file_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
            log_file_handler.setLevel(get_log_level(log_level))
            logger.addHandler(log_file_handler)
        return logger
