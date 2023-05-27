from datetime import datetime
import threading
import time

import schedule

from database.db_initializer import init_db
from service import chat_service, proposal_service, bot_service


def get_chats_and_save_latest_orders():
    chats = chat_service.get_chats()
    for chat in chats:
        proposals = proposal_service.find_newer_than(chat.last_message_datetime)
        for proposal in proposals:
            bot_service.send_proposal(chat.chat_id, proposal)
            pass
        chat.last_message_datetime = datetime.now()
        chat_service.update_chat(chat)
        pass
    pass


def start_scheduling():
    def scheduler():
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
    bot_thread = threading.Thread(target=bot_service.start())
    bot_thread.name = 'bot_thread'
    bot_thread.start()
    pass


def main():
    init_db()

    start_scheduling()

    init_bot()
    pass


if __name__ == '__main__':
    main()
