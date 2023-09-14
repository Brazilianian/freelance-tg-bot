from domain.chat.chat_state import ChatState
from domain.chat.chat_status import ChatStatus


class Chat:
    chat_id: int
    username: str
    first_name: str
    last_name: str
    last_message_datetime: str
    status: ChatStatus
    state: ChatState

    def __init__(self, chat_id: int,
                 username: str,
                 first_name: str,
                 last_name: str,
                 last_message_datetime: str,
                 status: ChatStatus,
                 state: ChatState):
        self.chat_id = chat_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.last_message_datetime = last_message_datetime
        self.status = status
        self.state = state

    def __str__(self):
        return f"chat_id - {self.chat_id}, " \
               f"username - {self.username}, " \
               f"first_name - {self.first_name}, " \
               f"last_name - {self.last_name}, " \
               f"last_message_datetime - {self.last_message_datetime}"

    def to_json(self):
        return {
            'chat_id': self.chat_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'last_message_datetime': self.last_message_datetime,
            'status': self.status.value,
            'state': self.state.value
        }
