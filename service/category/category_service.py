import json

from domain.HttpRequestType import HttpRequestType
from domain.category.category import Category
from domain.sites.freelance_site import FreelanceSite
from domain.sites.freelance_sites_enum import FreelanceSitesEnum
from service import requests_service, freelance_site_service


def get_categories_by_freelance_site(freelance_site: FreelanceSitesEnum):
    categories_json = json.loads(requests_service.send_http_request('/categories', HttpRequestType.GET,
                                                                    {'freelance_site': freelance_site.value},
                                                                    None))

    return from_json_to_list(categories_json)


def add_subscription_by_category_id(category_id: int,
                                    chat_id: int):
    requests_service.send_http_request(f'/categories/{category_id}/chats/{chat_id}',
                                       HttpRequestType.POST, None, None)


def get_category_by_id(category_id):
    category_json = json.loads(requests_service.send_http_request(f"/categories/{category_id}",
                                                                  HttpRequestType.GET,
                                                                  None, None))

    return from_json_to_object(category_json)


def add_subscription_all(freelance_site: FreelanceSitesEnum,
                         chat_id: int):
    requests_service.send_http_request(f"/freelanceSite/{freelance_site.value}/chats/{chat_id}",
                                       HttpRequestType.POST, None, None)


def from_json_to_list(categories_json):
    categories: [Category] = []
    for category_json in categories_json:
        categories.append(from_json_to_object(category_json))
    return categories


def from_json_to_object(category_json):
    freelance_site: FreelanceSite = freelance_site_service.from_json_to_object(category_json['freelance_site'])

    return Category(category_json['id'],
                    category_json['name'],
                    freelance_site_service.from_freelance_site_to_enum(freelance_site))
