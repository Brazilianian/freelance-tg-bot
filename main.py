from datetime import datetime
import threading
import time
from logger_configuration import logger

import schedule

from database.db_initializer import init_db
from logger_configuration.log_config import init_logger
from service import chat_service, proposal_service, bot_service


def get_chats_and_save_latest_orders():
    chats = chat_service.get_enabled_chats()
    for chat in chats:
        proposals = proposal_service.find_newer_than(chat.last_message_datetime)
        for proposal in proposals:
            bot_service.send_proposal(chat.chat_id, proposal)
            logger.info(f"Sent new proposal with link {proposal['link']} to chat with id {chat.chat_id}")
            pass

        chat_service.update_chat_last_message_datetime(chat.chat_id,
                                                       datetime.now())
        pass
    pass


def start_scheduling():
    def scheduler():
        logger.info("Starting scheduler")
        get_chats_and_save_latest_orders()

        schedule.every(20).seconds.do(get_chats_and_save_latest_orders)
        while True:
            schedule.run_pending()
            time.sleep(1)
            pass
        pass

    schedule_thread = threading.Thread(target=scheduler)
    schedule_thread.name = 'schedule_thread'
    schedule_thread.start()
    pass


def init_bot():
    logger.info("Starting bot")
    bot_thread = threading.Thread(target=bot_service.start())
    bot_thread.name = 'bot_thread'
    bot_thread.start()
    pass


def main():
    #FIXME the worst thing i`ve ever seen
    time.sleep(20)

    init_logger()
    init_db()
    start_scheduling()
    init_bot()
    pass


if __name__ == '__main__':
    main()
