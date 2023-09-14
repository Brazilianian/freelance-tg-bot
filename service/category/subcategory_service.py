import json

from domain.HttpRequestType import HttpRequestType
from domain.category.subcategory import Subcategory
from domain.chat.chat import Chat
from domain.sites.freelance_sites_enum import FreelanceSitesEnum
from service import requests_service
from service.category import category_service


def get_subcategories_by_freelance_site_and_chat_id(freelance_site: FreelanceSitesEnum,
                                                    chat_id: int):
    subcategories_json = json.loads(requests_service.send_http_request('/subcategories', HttpRequestType.GET, {
        'freelance_site': freelance_site.value,
        'chat_id': chat_id
    }, None))

    return from_json_to_list(subcategories_json)


def get_subcategories_by_category_id(category_id: int):
    subcategories_json = json.loads(requests_service.send_http_request(
        '/subcategories/category',
        HttpRequestType.GET,
        {'category_id': category_id},
        None))

    return from_json_to_list(subcategories_json)


def get_subcategories_of_chat(chat: Chat):
    subcategories_json = json.loads(requests_service.send_http_request('/subcategories/chats/' + str(chat.chat_id),
                                                                       HttpRequestType.GET, None, None))

    return from_json_to_list(subcategories_json)


def change_subscription(subcategory_id: int,
                        chat_id: int):
    requests_service.send_http_request(f'/subcategories/{subcategory_id}/chats/{chat_id}',
                                       HttpRequestType.POST, None, None)


def get_subcategory_by_id(subcategory_id):
    subcategory_json = json.loads(requests_service.send_http_request(f'/subcategories/{subcategory_id}',
                                                                     HttpRequestType.GET, None, None))

    return from_json_to_object(subcategory_json)


def from_json_to_list(subcategories_json):
    subcategories: [Subcategory] = []
    for subcategory_json in subcategories_json:
        subcategories.append(from_json_to_object(subcategory_json))

    return subcategories


def from_json_to_object(subcategory_json):
    return Subcategory(subcategory_json['id'],
                       subcategory_json['name'],
                       category_service.from_json_to_object(subcategory_json['category']))
