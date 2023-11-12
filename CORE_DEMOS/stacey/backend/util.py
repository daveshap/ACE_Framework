import json
import os

from dotenv import load_dotenv

load_dotenv()


def has_environment_variable(name):
    value = os.getenv(name)
    return value is not None and value.strip() != ""


def get_environment_variable(name):
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise EnvironmentError(f"{name} environment variable not set! Check your .env file.")

    return value


def parse_json(input_string):
    try:
        return json.loads(input_string)
    except json.JSONDecodeError:
        return None
