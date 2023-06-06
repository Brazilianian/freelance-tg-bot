from configparser import ConfigParser
from typing import Optional

import telebot
from telebot.apihelper import ApiTelegramException

from domain.chat_status import ChatStatus
from logger_configuration import logger
from repository import chat_repository
from service import proposal_service, chat_service
from service.chat_service import save_new_chat

config = ConfigParser()
config.read("tg.ini")

BOT_TOKEN = config["bot"]["API_TOKEN_TEST"]

bot = telebot.TeleBot(BOT_TOKEN)

WELCOME_MESSAGES = ["Hello, im a bot and i was create to send you new proposals from freelance sites.",
                    "Just wait and i will send you new records as soon as possible."]


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    for welcome_message in WELCOME_MESSAGES:
        send_message_to_chat(message.chat.id, welcome_message)
        pass

    save_new_chat(message.chat)
    pass


def send_proposal(chat_id, proposal):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text='Переглянути замовлення',
                                                url=f"{proposal['link']}")
    markup.add(button)

    send_message_to_chat(chat_id,
                         proposal_service.prettyfi_proposal(proposal),
                         reply_markup=markup)
    pass


def send_message_to_chat(chat_id: int,
                         message: str,
                         reply_markup: Optional[telebot.REPLY_MARKUP_TYPES] = None):
    try:
        bot.send_message(chat_id=chat_id,
                         text=message,
                         reply_markup=reply_markup)
    except ApiTelegramException as e:
        match e.error_code:
            case 403:
                chat = chat_service.get_by_chat_id(chat_id)
                logger.info(f"Chat {chat} was blocker by user")
                chat_service.update_chat_status(chat_id, ChatStatus.BLOCKED)
                pass
            case _:
                logger.error(str(e))
                pass
        pass
        pass
    pass


def start():
    bot.polling()
    pass
