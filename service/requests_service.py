import configparser
import json

import requests

from domain.HttpRequestType import HttpRequestType
from logger_configuration import logger

config = configparser.ConfigParser()
config.read('rest.ini')

BASE_URL = config["rest"]["BASE_URL"]


def send_http_request(url: str, http_type: HttpRequestType, params: object, json_data: json):
    try:
        response = send(url, http_type, params, json_data)

        if 200 <= response.status_code <= 299:
            return response.content
        else:
            logger.error(json.loads(response.content))
            return "[]"

    except requests.exceptions.ConnectionError as e:
        logger.error(str(e))
        return "[]"


def get_http_status(url: str,
                    http_type: HttpRequestType,
                    params: object,
                    json_data: json):
    try:
        return send(url, http_type, params, json_data).status_code
    except requests.exceptions.ConnectionError as e:
        logger.error(str(e))
    return "[]"


def send(url: str,
         http_type: HttpRequestType,
         params: object,
         json_data: json):
    match http_type:
        case HttpRequestType.GET:
            return requests.get(url=BASE_URL + url,
                                params=params,
                                json=json_data)
        case HttpRequestType.POST:
            return requests.post(url=BASE_URL + url,
                                 params=params,
                                 json=json_data)
        case HttpRequestType.PUT:
            return requests.put(url=BASE_URL + url,
                                params=params,
                                json=json_data)
        case _:
            logger.error("Invalid http type")
            return None
