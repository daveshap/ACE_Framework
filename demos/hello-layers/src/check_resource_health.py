#!/usr/bin/env python3

import sys
import logging
import requests

from ace.logger import Logger

logger = Logger(__name__)

HOST = 'http://localhost:3000'


def main():
    logger.debug("Checking resource health...")
    try:
        response = requests.get(f"{HOST}/status")
        if response.status_code == 200:
            data = response.json()
            if "up" in data and data["up"] is True:
                return sys.exit(0)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        logging.error("Unknown error:", err)
        sys.exit(1)
    except requests.exceptions.HTTPError as errh:
        logging.error("HTTP error:", errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        logging.error("Connection error:", errc)
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout error:", errt)
        sys.exit(1)


if __name__ == '__main__':
    main()
