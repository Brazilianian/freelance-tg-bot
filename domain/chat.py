class Chat:
    chat_id = 0
    last_message_datetime = ""

    def __init__(self, chat_id, last_message_datetime):
        self.chat_id = chat_id
        self.last_message_datetime = last_message_datetime
        pass

    def __str__(self):
        return f"chat_id - {self.chat_id}\n" \
               f"last_message_datetime - {self.last_message_datetime}"

    pass
