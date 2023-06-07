from datetime import datetime

from domain.chat import Chat
from logger_configuration import logger
from model.chat_model import ChatModel


def save(chat: Chat):
    chat_model: ChatModel = ChatModel.create(
        chat_id=chat.chat_id,
        username=chat.username,
        first_name=chat.first_name,
        last_name=chat.last_name,
        last_message_datetime=chat.last_message_datetime
    )

    return chat_model.save()
    pass


def get_by_chat_id(chat_id: int):
    query = ChatModel.select().where(ChatModel.chat_id == chat_id)
    return query.execute()
    pass


def find_all():
    query = ChatModel.select()
    return query.execute()


def update_last_message_datetime(chat_id: int,
                                 message_datetime: datetime):
    query = ChatModel \
        .update(last_message_datetime=message_datetime) \
        .where(ChatModel.chat_id == chat_id)

    query.execute()
    logger.info(f"Updated last_message_datetime='{message_datetime}' to chat with id '{chat_id}'")
    pass


def update_status(chat_id: int,
                  status: str):
    query = ChatModel \
        .update(status=status) \
        .where(ChatModel.chat_id == chat_id)

    query.execute()
    logger.info(f"Updated status='{status}' to chat with id '{chat_id}'")
    pass


def find_by_status(status):
    query = ChatModel.select().where(ChatModel.status == status)
    return query.execute()
