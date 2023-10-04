import logging

from ace import constants

# Set the logger for pika, aiormq separately.
for base_logger in constants.THIRD_PARTY_LOGGERS:
    logging.getLogger(base_logger).setLevel(constants.THIRD_PARTY_LOG_LEVEL)


class Logger:
    def __new__(cls, name):
        logger = logging.getLogger(name)
        # Prevent duplicate loggers.
        if logger.hasHandlers():
            return logger
        logger.setLevel(logging.DEBUG)
        log_console_handler = logging.StreamHandler()
        log_console_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
        log_console_handler.setLevel(constants.LOG_LEVEL)
        logger.addHandler(log_console_handler)
        if constants.LOG_FILEPATH:
            log_file_handler = logging.FileHandler(constants.LOG_FILEPATH, "a")
            log_file_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
            log_file_handler.setLevel(constants.LOG_LEVEL)
            logger.addHandler(log_file_handler)
        return logger
