from peewee import *

from model.base_model import BaseModel


class ChatModel(BaseModel):
    chat_id = BigIntegerField(primary_key=True)
    last_message_datetime = DateTimeField()

    def __str__(self):
        return f"chat_id - {self.chat_id}\n" \
               f"last_message_datetime - {self.last_message_datetime}"

    class Meta:
        table_name = 'chats'


pass
