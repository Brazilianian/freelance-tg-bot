from database.db_config import db
from model.chat_model import ChatModel


def init_db():
    db.connect()
    if not ChatModel.table_exists():
        ChatModel.create_table()
        pass
    pass
