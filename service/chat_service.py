from datetime import datetime

from domain.chat import Chat
from repository import chat_repository
from repository.chat_repository import save, get_by_chat_id


def is_chat_already_exists(chat_id):
    chats = get_by_chat_id(chat_id)
    return len(chats) > 0
    pass


def save_new_chat(chat_id: int):
    if not is_chat_already_exists(chat_id):
        chat = Chat(chat_id, datetime.now().strftime("%Y-%m-%d 00:00:00"))
        save(chat)
        pass
    pass


def get_chats():
    return chat_repository.find_all()


def update_chat(chat):
    chat_repository.update(chat)
    return None
