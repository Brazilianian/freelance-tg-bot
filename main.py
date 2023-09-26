import threading
import time
from datetime import datetime

import schedule

from domain.proposal import Proposal
from logger_configuration import logger
from logger_configuration.log_config import init_logger
from service import chat_service, proposal_service, bot_service


def get_chats_and_send_latest_orders():
    chats = chat_service.get_enabled_chats()
    for chat in chats:
        proposals: [Proposal] = proposal_service.find_newer_than(chat.last_message_datetime)
        proposals = proposal_service.filter_by_chat_subscription(proposals,
                                                                 chat)
        for proposal in proposals:
            bot_service.send_proposal(chat.chat_id, proposal)
            logger.info(f"Sent new proposal with link {proposal.link} to chat with id {chat.chat_id}")

        chat_service.update_chat_last_message_datetime(chat.chat_id,
                                                       datetime.now())


def start_scheduling():
    def scheduler():
        logger.info("Starting scheduler")
        get_chats_and_send_latest_orders()

        schedule.every(20).seconds.do(get_chats_and_send_latest_orders)
        while True:
            schedule.run_pending()
            time.sleep(1)

    schedule_thread = threading.Thread(target=scheduler)
    schedule_thread.name = 'schedule_thread'
    schedule_thread.start()


def init_bot():
    try:
        logger.info("Starting bot")
        bot_thread = threading.Thread(target=bot_service.start())
        bot_thread.name = 'bot_thread'
        bot_thread.start()
    except:
        time.sleep(1000)
        init_bot()


if __name__ == '__main__':
    print("Starting App")
    init_logger()
    start_scheduling()
    init_bot()
