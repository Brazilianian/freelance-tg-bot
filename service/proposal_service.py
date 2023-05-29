import requests
import json

BASE_URL = 'http://localhost:8080/api/v1'


def find_newer_than(last_message_datetime):
    response = requests.get(url=BASE_URL + '/proposals',
                            params={
                                'date': last_message_datetime
                            })
    proposals = json.loads(response.content)
    return proposals


def prettyfi_proposal(proposal):
    string = f"{proposal['title']}\n\n" \
             f"{proposal['price']}\n\n" \
             f"{proposal['description']}\n\n" \

    for tag in proposal['additional_info_tags']:
        string += f"{tag} | "
        pass
    return string[:-2]
