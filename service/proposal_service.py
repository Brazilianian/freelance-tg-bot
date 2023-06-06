from service.requests_service import send_http_request


def find_newer_than(last_message_datetime):
    return send_http_request('/requests', 'GET', {
        'date': last_message_datetime
    })


def prettyfi_proposal(proposal):
    string = f"{proposal['title']}\n\n" \
             f"{proposal['price']}\n\n" \
             f"{proposal['description']}\n\n"

    for tag in proposal['additional_info_tags']:
        string += f"{tag} | "
        pass

    return string[:-2]
