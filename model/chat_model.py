from peewee import *

from model.base_model import BaseModel


class ChatModel(BaseModel):
    chat_id = BigIntegerField(primary_key=True)
    last_message_datetime = DateTimeField()
    username = TextField(null=True)
    first_name = TextField(null=True)
    last_name = TextField(null=True)
    status = TextField(default='ENABLED')
    state = TextField(default='START')

    def __str__(self):
        return f"chat_id - {self.chat_id} " \
               f"username - {self.username} " \
               f"first_name - {self.first_name} " \
               f"last_name - {self.last_name} " \
               f"status - {self.status} " \
               f"state - {self.state} " \
               f"last_message_datetime - {self.last_message_datetime}"

    class Meta:
        table_name = 'chats'
