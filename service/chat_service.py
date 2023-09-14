import json
from datetime import datetime

import telebot.types

from domain.HttpRequestType import HttpRequestType
from domain.chat.chat import Chat
from domain.chat.chat_state import ChatState
from domain.chat.chat_status import ChatStatus
from service import requests_service


def is_chat_already_exists(chat_id: int):
    return False if requests_service.get_http_status(f'/chats/{chat_id}', HttpRequestType.GET,
                                                     None, None) == 404 else True


def save_new_chat(chat: telebot.types.Chat):
    if not is_chat_already_exists(chat.id):
        chat = Chat(chat_id=chat.id,
                    username=chat.username,
                    first_name=chat.first_name,
                    last_name=chat.last_name,
                    status=ChatStatus.ENABLED,
                    state=ChatState.START,
                    last_message_datetime=datetime.now().strftime("%Y-%m-%d 00:00:00"))

        requests_service.send_http_request(f'/chats', HttpRequestType.POST, None, chat.to_json())
    else:
        update_chat_status(chat.id, ChatStatus.ENABLED)
        update_chat_last_message_datetime(chat.id, datetime.now())
    pass


def get_chats():
    chats_json = json.loads(requests_service.send_http_request('/chats', HttpRequestType.GET, None, None))

    return from_json_to_list(chats_json)


def update_chat_last_message_datetime(chat_id: int,
                                      message_datetime: datetime):
    chat_json = json.loads(requests_service.send_http_request(f'/chats/{chat_id}/last_message_datetime',
                                                              HttpRequestType.PUT,
                                                              {'last_message_datetime': message_datetime.strftime(
                                                                  "%Y-%m-%d %H:%M:%S")},
                                                              None))

    return from_json_to_object(chat_json)


def update_chat_status(chat_id: int,
                       status: ChatStatus):
    chat_json = json.loads(requests_service.send_http_request(f'/chats/{chat_id}/status',
                                                              HttpRequestType.PUT,
                                                              {'status': status.value}, None))
    return from_json_to_object(chat_json)


def update_chat_state(chat_id: int,
                      chat_state: ChatState):
    chat_json = json.loads(requests_service.send_http_request(f'/chats/{chat_id}/state',
                                                              HttpRequestType.PUT,
                                                              {'state': chat_state.value}, None))

    return from_json_to_object(chat_json)


def get_enabled_chats():
    chats_json = json.loads(requests_service.send_http_request('/chats', HttpRequestType.GET, {
        'status': ChatStatus.ENABLED.value
    }, None))

    return from_json_to_list(chats_json)


def get_by_chat_id(chat_id: int):
    chat_json = json.loads(requests_service.send_http_request(f'/chats/{chat_id}',
                                                              HttpRequestType.GET,
                                                              None, None))

    return from_json_to_object(chat_json)


def from_json_to_list(chats_json):
    chats: [Chat] = []
    for chat_json in chats_json:
        chats.append(from_json_to_object(chat_json))
    return chats


def from_json_to_object(chat_json):
    return Chat(int(chat_json['chat_id']),
                chat_json['username'],
                chat_json['first_name'],
                chat_json['last_name'],
                chat_json['last_message_datetime'],
                getattr(ChatStatus, chat_json['status']),
                getattr(ChatState, chat_json['state']))
