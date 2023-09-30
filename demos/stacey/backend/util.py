import os

from dotenv import load_dotenv

load_dotenv()


def get_environment_variable(name):
    value = os.getenv(name)
    if value is None:
        raise EnvironmentError(f"{name} environment variable not set! Check your .env file.")
    return value
