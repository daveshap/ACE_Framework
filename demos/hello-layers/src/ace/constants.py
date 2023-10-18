# LAYER_SLEEP_TIME = 5
# LAYER_1_DECLARE_DONE_MESSAGE_COUNT = 5
LAYER_SLEEP_TIME = 10000000
LAYER_1_DECLARE_DONE_MESSAGE_COUNT = 2
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
    'docker',
    'urllib3',
    'openai',
    'httpx',
    'httpcore',
]
THIRD_PARTY_LOG_LEVEL = "WARNING"
DEFAULT_API_ENDPOINT_PORT: int = 3000
DEFAULT_DEBUG_ENDPOINT_PORT: int = 4000
DEFAULT_DEBUG_UI_ENDPOINT_PORT: int = 4001
