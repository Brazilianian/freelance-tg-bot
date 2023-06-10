import configparser

from domain.freelance_site import FreelanceSite
from domain.proposal import Proposal
from service import freelance_site_service, telegram_message_service
from service.requests_service import send_http_request
from service.telegram_message_service import set_bold, set_italic

config = configparser.ConfigParser()
config.read('rest.ini')

BASE_URL = config["rest"]["BASE_URL"]


def find_newer_than(last_message_datetime):
    proposals_json = send_http_request('/proposals', 'GET', {
        'date': last_message_datetime
    })

    proposals = []
    for proposal_json in proposals_json:
        proposals.append(from_json_to_object(proposal_json))
    return proposals

def from_json_to_object(proposal):
    freelance_site: FreelanceSite = freelance_site_service.from_json_to_object(proposal['freelance_site'])

    return Proposal(int(proposal['id']),
                    proposal['title'],
                    proposal['price'],
                    proposal['description'],
                    proposal['link'],
                    proposal['additional_info_tags'],
                    proposal['posted_date'],
                    freelance_site)


def prettyfi_proposal(proposal: Proposal):
    pretty = f"{set_italic(set_bold(proposal.title))}\n\n"

    pretty += f"{proposal.description}\n\n"

    if proposal.price != '':
        pretty += f"💰 {set_bold(proposal.price)}\n\n"

    match proposal.freelance_site.name:
        case "freelance.ua":
            pretty += f"🟩 Freelance ua\n\n"
        case "freelancehunt.com":
            pretty += f"🟧 Freelance Hunt\n\n"

    if not len(proposal.additional_info_tags) == 0 and not proposal.additional_info_tags[0] == '':
        pretty += "📣 "
        for tag in proposal.additional_info_tags:
            pretty += f"{tag} | "

    return pretty[:-2]
