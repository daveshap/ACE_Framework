LAYER_ORIENTATIONS = [
    'northbound',
    'southbound',
]
QUEUE_SUBSCRIBE_RETRY_SECONDS = 5

# Logging.
LOG_LEVEL = "INFO"
LOG_FILEPATH = None
LOG_FORMAT = "%(name)s - %(levelname)s - %(message)s"
THIRD_PARTY_LOGGERS = [
    'aio_pika',
    'aiormq',
    'asyncio',
]
THIRD_PARTY_LOG_LEVEL = "WARNING"
