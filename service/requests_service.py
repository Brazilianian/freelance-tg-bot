import configparser
import requests
import json

from logger_configuration import logger

config = configparser.ConfigParser()
config.read('rest.ini')

BASE_URL = config["rest"]["BASE_URL"]


def send_http_request(url: str, http_type: str, params: object):
    response = []
    try:
        match http_type.lower().strip():
            case "get":
                response = requests.get(BASE_URL + url, params)
                pass
            case "pots":
                response = requests.post(BASE_URL + url, params)
                pass
            case _:
                logger.error("Invalid http type")
                return ""
                pass

        if 200 <= response.status_code <= 299:
            return json.loads(response.content)
        else:
            logger.error(json.loads(response.content))
            return []
            pass

        pass
    except requests.exceptions.ConnectionError as e:
        logger.error(str(e))
        return []
        pass


pass