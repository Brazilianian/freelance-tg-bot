from configparser import ConfigParser

import telebot

from service import proposal_service
from service.chat_service import save_new_chat

config = ConfigParser()
config.read("tg.ini")

BOT_TOKEN = config["bot"]["API_TOKEN"]

bot = telebot.TeleBot(BOT_TOKEN)

WELCOME_MESSAGES = ["Hello, im a bot and i was create to send you new proposals from freelance sites.",
                    "Just wait and i will send you new records as soon as possible."]


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    for welcome_message in WELCOME_MESSAGES:
        bot.send_message(message.chat.id, welcome_message)

    save_new_chat(message.chat.id)
    pass


def send_proposal(chat_id, proposal):
    bot.send_message(chat_id, proposal_service.prettyfi_proposal(proposal))
    pass


def start():
    bot.polling()
    pass
