import configparser
import json

from domain.HttpRequestType import HttpRequestType
from domain.category.subcategory import Subcategory
from domain.chat.chat import Chat
from domain.proposal import Proposal
from domain.sites.freelance_site import FreelanceSite
from domain.sites.freelance_sites_enum import FreelanceSitesEnum
from service import freelance_site_service, telegram_message_service
from service.category import subcategory_service
from service.requests_service import send_http_request

config = configparser.ConfigParser()
config.read('rest.ini')

BASE_URL = config["rest"]["BASE_URL"]


def find_newer_than(last_message_datetime):
    proposals_json = json.loads(send_http_request('/proposals', HttpRequestType.GET, {
        'date': last_message_datetime
    }, None))

    return from_json_to_list(proposals_json)


def from_json_to_list(proposals_json):
    proposals: [Proposal] = []
    for proposal_json in proposals_json:
        proposals.append(from_json_to_object(proposal_json))

    return proposals


def from_json_to_object(proposal):
    freelance_site: FreelanceSite = freelance_site_service.from_json_to_object(proposal['freelance_site'])
    subcategories: [Subcategory] = []
    for subcategory_json in proposal['subcategories']:
        subcategories.append(subcategory_service.from_json_to_object(subcategory_json))

    return Proposal(int(proposal['id']),
                    proposal['title'],
                    proposal['price'],
                    proposal['description'],
                    proposal['link'],
                    proposal['additional_info_tags'],
                    proposal['posted_date'],
                    freelance_site,
                    subcategories)


def prettyfi_proposal(proposal: Proposal):
    pretty = f"{telegram_message_service.set_italic(telegram_message_service.set_bold(proposal.title))}\n\n"

    pretty += f"{proposal.description}\n\n"

    if proposal.price != '':
        pretty += f"💰 {telegram_message_service.set_bold(proposal.price)}\n\n"

    match proposal.freelance_site.name:
        case FreelanceSitesEnum.FREELANCE_UA.value:
            pretty += f"🟩 Freelance ua\n\n"  # Green square
        case FreelanceSitesEnum.FREELANCE_HUNT.value:
            pretty += f"🟧 Freelance Hunt\n\n"  # Orange square

    if not len(proposal.additional_info_tags) == 0 and not proposal.additional_info_tags[0] == '':
        pretty += "📣 "
        for tag in proposal.additional_info_tags:
            pretty += f"{tag} | "

    return pretty[:-2]


def filter_by_chat_subscription(proposals: [Proposal],
                                chat: Chat):
    filtered_proposals: [Proposal] = []
    subscriptions: [Subcategory] = subcategory_service.get_subcategories_of_chat(chat)

    # If user doesn't have any subscription - send every order
    if len(subscriptions) == 0:
        return proposals

    subcategories_ids = [subcategory.id for subcategory in subscriptions]
    for proposal in proposals:
        for subcategory in proposal.subcategories:
            if subcategory.id in subcategories_ids:
                filtered_proposals.append(proposal)
                break
    return filtered_proposals
