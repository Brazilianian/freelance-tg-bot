from domain.category.category import Category
from domain.sites.freelance_site import FreelanceSite
from domain.sites.freelance_sites_enum import FreelanceSitesEnum
from service import requests_service, freelance_site_service


def get_categories_by_freelance_site(freelance_site: FreelanceSitesEnum):
    categories_json = requests_service.send_http_request('/categories', 'GET', {
        'freelance_site': freelance_site.value
    })

    categories = []
    for category_json in categories_json:
        categories.append(from_json_to_object(category_json))

    return categories


def from_json_to_object(category_json):
    freelance_site: FreelanceSite = freelance_site_service.from_json_to_object(category_json['freelance_site'])

    return Category(category_json['id'],
                    category_json['name'],
                    freelance_site_service.from_freelance_site_to_enum(freelance_site))


def add_subscription_by_category_id(category_id: int,
                                    chat_id: int):
    requests_service.send_http_request(f'/categories/{category_id}/chats/{chat_id}', 'POST', {})


def get_category_by_id(category_id):
    category_json = requests_service.send_http_request(f"/categories/{category_id}", 'GET', {})
    return from_json_to_object(category_json)


def add_subscription_all(freelance_site: FreelanceSitesEnum,
                         chat_id: int):
    requests_service.send_http_request(f"/freelanceSite/{freelance_site.value}/chats/{chat_id}", 'POST', {})
