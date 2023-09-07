from datetime import datetime

import telebot.types

from domain.chat.chat import Chat
from domain.chat.chat_state import ChatState
from domain.chat.chat_status import ChatStatus
from repository import chat_repository
from repository.chat_repository import save, get_by_chat_id


def is_chat_already_exists(chat_id):
    chats = get_by_chat_id(chat_id)
    return len(chats) > 0


def save_new_chat(chat: telebot.types.Chat):
    if not is_chat_already_exists(chat.id):
        chat = Chat(chat_id=chat.id,
                    username=chat.username,
                    first_name=chat.first_name,
                    last_name=chat.last_name,
                    last_message_datetime=datetime.now().strftime("%Y-%m-%d 00:00:00"))
        save(chat)
    else:
        update_chat_status(chat.id, ChatStatus.ENABLED)
        update_chat_last_message_datetime(chat.id, datetime.now())


def get_chats():
    return chat_repository.find_all()


def update_chat_last_message_datetime(chat_id: int, message_datetime: datetime):
    return chat_repository.update_last_message_datetime(chat_id,
                                                 message_datetime)


def update_chat_status(chat_id: int,
                       status: ChatStatus):
    return chat_repository.update_status(chat_id, status.value)


def get_enabled_chats():
    return chat_repository.find_by_status(ChatStatus.ENABLED.value)


def update_chat_state(chat_id: int, chat_state: ChatState):
    return chat_repository.update_chat_state_by_chat_id(chat_id, chat_state.value)
