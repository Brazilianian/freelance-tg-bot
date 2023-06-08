from database.db_config import db
from logger_configuration import logger
from model.chat_model import ChatModel


def init_db():
    db.connect()
    logger.info("Database connected")
    if not ChatModel.table_exists():
        ChatModel.create_table()
        logger.info("Table created")
