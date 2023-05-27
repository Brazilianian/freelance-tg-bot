from domain.chat import Chat
from model.chat_model import ChatModel


def save(chat: Chat):
    chat_model: ChatModel = ChatModel.create(
        chat_id=chat.chat_id,
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


def update(chat):
    query = ChatModel.update(last_message_datetime=chat.last_message_datetime)
    query.execute()
    pass
