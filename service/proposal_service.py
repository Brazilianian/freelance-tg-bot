import configparser

from service.requests_service import send_http_request

config = configparser.ConfigParser()
config.read('rest.ini')

BASE_URL = config["rest"]["BASE_URL"]


def find_newer_than(last_message_datetime):
    return send_http_request('/proposals', 'GET', {
        'date': last_message_datetime
    })


def prettyfi_proposal(proposal):
    string = f"<strong>{proposal['freelance_site']['name']}</strong>" \
             f"{proposal['title']}\n\n" \
             f"{proposal['price']}\n\n" \
             f"{proposal['description']}\n\n" \

    for tag in proposal['additional_info_tags']:
        string += f"{tag} | "

    return string[:-2]
