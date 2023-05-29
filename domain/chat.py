class Chat:
    chat_id = 0
    username = ""
    first_name = ""
    last_name = ""
    last_message_datetime = ""

    def __init__(self, chat_id, username, first_name, last_name, last_message_datetime):
        self.chat_id = chat_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.last_message_datetime = last_message_datetime
        pass

    def __str__(self):
        return f"chat_id - {self.chat_id}, " \
               f"username - {self.username}, " \
               f"first_name - {self.first_name}, " \
               f"last_name - {self.last_name}, " \
               f"last_message_datetime - {self.last_message_datetime}"

    pass
