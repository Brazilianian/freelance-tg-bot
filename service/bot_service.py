import time
from configparser import ConfigParser
from typing import Optional

import telebot
from requests import ConnectTimeout
from telebot.apihelper import ApiTelegramException

from domain.category.category import Category
from domain.category.subcategory import Subcategory
from domain.chat.chat import Chat
from domain.chat.chat_state import ChatState
from domain.chat.chat_status import ChatStatus
from domain.proposal import Proposal
from domain.sites.freelance_sites_enum import FreelanceSitesEnum
from logger_configuration import logger
from service import proposal_service, chat_service, telegram_message_service
from service.category import subcategory_service, category_service

config = ConfigParser()
config.read("tg.ini")

BOT_TOKEN = config["bot"]["API_TOKEN"]

bot = telebot.TeleBot(BOT_TOKEN)
WELCOME_MESSAGES = ["Hello, im a bot was created to send you new proposals from freelance sites.",
                    "First of all manage your subscriptions /subs to choose type of proposals you wish to receive"]

SUBS_MESSAGES = ["Subscription Settings: Here, you can manage the types of proposals you wish to receive.\n\n"
                 "First, choose the site you want to manage:\n"]


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    chat_service.save_new_chat(message.chat)
    chat_service.update_chat_state(message.chat.id, ChatState.START)

    for welcome_message in WELCOME_MESSAGES:
        send_message_to_chat(message.chat.id,
                             welcome_message)


@bot.message_handler(commands=['subs'])
def send_subs_management(message: telebot.types.Message):
    freelance_sites: [FreelanceSitesEnum] = [fs for fs in FreelanceSitesEnum]
    chat: Chat = chat_service.get_by_chat_id(message.chat.id)

    markup = telebot.types.InlineKeyboardMarkup()

    for freelance_site in freelance_sites:
        categories: [Category] = category_service.get_categories_by_freelance_site(freelance_site)
        subscriptions: [Subcategory] = subcategory_service.get_subcategories_of_chat(chat)

        count_of_subcategories: int = 0
        count_founded_subs: int = 0

        for c in categories:
            subcategories: [Subcategory] = subcategory_service.get_subcategories_by_category_id(c.id)
            for sub in subcategories:
                count_of_subcategories += 1
                if sub.id in [subscription.id for subscription in subscriptions]:
                    count_founded_subs += 1

        if count_founded_subs == count_of_subcategories:
            markup.add(telebot.types.InlineKeyboardButton(text=freelance_site.value + " ✅",
                                                          callback_data=freelance_site.value))
        elif count_founded_subs == 0:
            markup.add(telebot.types.InlineKeyboardButton(text=freelance_site.value + " ❌",
                                                          callback_data=freelance_site.value))
        else:
            markup.add(telebot.types.InlineKeyboardButton(text=freelance_site.value + " ➖",
                                                          callback_data=freelance_site.value))

    markup.add(telebot.types.InlineKeyboardButton(text="<== Go Back <==",
                                                  callback_data="Back START"))
    for sub_message in SUBS_MESSAGES:
        send_message_to_chat(chat_id=message.chat.id,
                             message=sub_message,
                             reply_markup=markup,
                             parse_mode='HTML')

    chat_service.update_chat_state(message.chat.id, ChatState.SUBS)


@bot.callback_query_handler(func=lambda call: call.data.startswith('SUBS_'))
def subs_add_remove_callback_handler(call):
    chat = chat_service.get_by_chat_id(call.message.chat.id)
    match call.data:
        case "SUBS_FU_ADD":
            bot.answer_callback_query(call.id)
            add_subscription_choose_category(FreelanceSitesEnum.FREELANCE_UA,
                                             chat)
            chat_service.update_chat_state(chat.chat_id,
                                           ChatState.SUBS_FU)
        case "SUBS_FH_ADD":
            bot.answer_callback_query(call.id)
            add_subscription_choose_category(FreelanceSitesEnum.FREELANCE_HUNT,
                                             chat)
            chat_service.update_chat_state(chat.chat_id,
                                           ChatState.SUBS_FH)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Back'))
def go_back_callback_handler(call):
    chat = chat_service.get_by_chat_id(call.message.chat.id)
    match call.data:
        case "Back START":
            chat_service.update_chat_state(chat.chat_id,
                                           ChatState.START)
            send_message_to_chat(chat.chat_id,
                                 "Everything is set up! Just wait for new messages 🧐")
        case "Back SUBS":
            send_subs_management(call.message)
        case "Back CATEGORY":
            freelance_site: FreelanceSitesEnum = FreelanceSitesEnum.FREELANCE_UA
            match chat.state:
                case ChatState.SUBS_FU:
                    freelance_site = FreelanceSitesEnum.FREELANCE_UA
                case ChatState.SUBS_FH:
                    freelance_site = FreelanceSitesEnum.FREELANCE_HUNT

            add_subscription_choose_category(freelance_site,
                                             chat)
    try:
        bot.delete_message(chat.chat_id,
                           call.message.id)
        bot.answer_callback_query(call.id)
    except:
        pass


@bot.callback_query_handler(func=lambda call: call.data.startswith('freelance'))
def freelance_sites_subscriptions_callback_handler(call):
    chat = chat_service.get_by_chat_id(call.message.chat.id)
    freelance_site: FreelanceSitesEnum

    match call.data:
        case FreelanceSitesEnum.FREELANCE_UA.value:
            freelance_site = FreelanceSitesEnum.FREELANCE_UA
            chat_service.update_chat_state(call.message.chat.id,
                                           ChatState.SUBS_FU)

        case FreelanceSitesEnum.FREELANCE_HUNT.value:
            freelance_site = FreelanceSitesEnum.FREELANCE_HUNT
            chat_service.update_chat_state(call.message.chat.id,
                                           ChatState.SUBS_FH)
        case _:
            return

    add_subscription_choose_category(freelance_site,
                                     chat)
    try:
        bot.delete_message(chat.chat_id,
                           call.message.id)
        bot.answer_callback_query(call.id)
    except:
        pass


@bot.callback_query_handler(func=lambda call: call.data.startswith('CATEGORY'))
def choose_subcategory_query_handler(call):
    category_id = int(str(call.data).split('_')[1])
    chat = chat_service.get_by_chat_id(call.message.chat.id)

    if len(str(call.data).split('_')) == 3 and str(call.data).split('_')[2] == "ALL":
        category = category_service.get_category_by_id(category_id)
        freelance_site: FreelanceSitesEnum = category.freelance_site
        category_service.add_subscription_all(freelance_site,
                                              chat.chat_id)
        add_subscription_choose_category(freelance_site,
                                         chat)
    else:
        category_id = int(category_id)

        add_subscription_choose_subcategory(category_id,
                                            chat)
    try:
        bot.delete_message(chat.chat_id,
                           call.message.id)
        bot.answer_callback_query(call.id)
    except:
        pass


@bot.callback_query_handler(func=lambda call: call.data.startswith('SUBCATEGORY'))
def choose_subcategory_to_subscribe_query_handler(call):
    subcategory_id = int(str(call.data).split('_')[1])
    chat = chat_service.get_by_chat_id(call.message.chat.id)
    subcategory = subcategory_service.get_subcategory_by_id(subcategory_id)

    # Select All
    if len(str(call.data).split('_')) == 3 and str(call.data).split('_')[2] == "ALL":
        category_service.add_subscription_by_category_id(subcategory.category.id,
                                                         chat.chat_id)
    else:
        subcategory_service.change_subscription(subcategory_id,
                                                chat.chat_id)

    add_subscription_choose_subcategory(subcategory.category.id,
                                        chat)
    try:
        bot.answer_callback_query(call.id)
        bot.delete_message(chat.chat_id,
                           call.message.id)
    except:
        pass


def send_proposal(chat_id: int,
                  proposal: Proposal):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text='Переглянути замовлення',
                                                url=f"{proposal.link}")
    markup.add(button)

    send_message_to_chat(chat_id,
                         proposal_service.prettyfi_proposal(proposal),
                         reply_markup=markup,
                         parse_mode="HTML")


def add_subscription_choose_category(freelance_site: FreelanceSitesEnum,
                                     chat: Chat):
    categories: [Category] = category_service.get_categories_by_freelance_site(freelance_site)
    subscriptions: [Subcategory] = subcategory_service.get_subcategories_of_chat(chat)

    markup = telebot.types.InlineKeyboardMarkup()
    for c in categories:
        count_founded_subs: int = 0
        for sub in subscriptions:
            if sub.category.id == c.id:
                count_founded_subs += 1

        subcategories: [Subcategory] = subcategory_service.get_subcategories_by_category_id(c.id)
        if count_founded_subs == len(subcategories):
            markup.add(telebot.types.InlineKeyboardButton(text=c.name + " ✅",
                                                          callback_data='CATEGORY_' + str(c.id)))
        elif count_founded_subs == 0:
            markup.add(telebot.types.InlineKeyboardButton(text=c.name + " ❌",
                                                          callback_data='CATEGORY_' + str(c.id)))
        else:
            markup.add(telebot.types.InlineKeyboardButton(text=c.name + " ➖",
                                                          callback_data='CATEGORY_' + str(c.id)))

    markup.add(telebot.types.InlineKeyboardButton(text="Select All",
                                                  callback_data="CATEGORY_" + str(categories[0].id) + "_ALL"))

    markup.add(telebot.types.InlineKeyboardButton(text="<== Go Back <==",
                                                  callback_data="Back SUBS"))

    markup.add(telebot.types.InlineKeyboardButton(text="✔ Complete ✔",
                                                  callback_data="Back START"))
    send_message_to_chat(chat_id=chat.chat_id,
                         message=f"{telegram_message_service.set_bold(telegram_message_service.set_italic(freelance_site.value))}\n\n"
                                 f"Choose category then check type of proposals you with to receive:",
                         reply_markup=markup)


def add_subscription_choose_subcategory(category_id: int,
                                        chat: Chat):
    subcategories: [Subcategory] = subcategory_service.get_subcategories_by_category_id(category_id)
    subscriptions: [Subcategory] = subcategory_service.get_subcategories_of_chat(chat)

    markup = telebot.types.InlineKeyboardMarkup()
    for subc in subcategories:
        if subc.id in [subscription.id for subscription in subscriptions]:
            markup.add(telebot.types.InlineKeyboardButton(text=subc.name + " ✅",
                                                          callback_data="SUBCATEGORY_" + str(subc.id)))
        else:
            markup.add(telebot.types.InlineKeyboardButton(text=subc.name + " ❌",
                                                          callback_data="SUBCATEGORY_" + str(subc.id)))

    markup.add(telebot.types.InlineKeyboardButton(text="Select All",
                                                  callback_data="SUBCATEGORY_" + str(subcategories[0].id) + "_ALL"))

    markup.add(telebot.types.InlineKeyboardButton(text="<== Go Back <==",
                                                  callback_data="Back CATEGORY"))

    markup.add(telebot.types.InlineKeyboardButton(text="✔ Complete ✔",
                                                  callback_data="Back START"))
    send_message_to_chat(chat_id=chat.chat_id,
                         message=f"{telegram_message_service.set_bold(telegram_message_service.set_italic(subcategories[0].category.freelance_site.value))}"
                                 f" ==> {telegram_message_service.set_italic(subcategories[0].category.name)}\n\n"
                                 "Choose type of proposal to receive:",
                         reply_markup=markup)


def send_message_to_chat(chat_id: int,
                         message: str,
                         reply_markup: Optional[telebot.REPLY_MARKUP_TYPES] = None,
                         parse_mode: Optional[str] = "HTML"):
    try:
        return bot.send_message(chat_id=chat_id,
                                text=message,
                                reply_markup=reply_markup,
                                parse_mode=parse_mode)
    except ApiTelegramException as e:
        match e.error_code:
            case 403:
                chat = chat_service.get_by_chat_id(chat_id)
                logger.info(f"Chat {chat} was blocker by user")
                chat_service.update_chat_status(chat_id, ChatStatus.BLOCKED)
            case _:
                logger.error(str(e))
    except ConnectTimeout as ct:
        logger.error(str(ct))
        time.sleep(1000)
        return send_message_to_chat(chat_id, message, reply_markup, parse_mode)

    return None


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    logger.info(f'/start command by chat with id {message.chat.id}')
    for welcome_message in WELCOME_MESSAGES:
        send_message_to_chat(message.chat.id,
                             welcome_message)

    chat_service.save_new_chat(message.chat)
    chat_service.update_chat_state(message.chat.id, ChatState.START)


@bot.message_handler(commands=['subs'])
def send_subs_management(message: telebot.types.Message):
    logger.info(f'/subs command by chat with id {message.chat.id}')
    freelance_sites: [FreelanceSitesEnum] = [fs for fs in FreelanceSitesEnum]
    chat: Chat = chat_service.get_by_chat_id(message.chat.id)

    markup = telebot.types.InlineKeyboardMarkup()

    for freelance_site in freelance_sites:
        categories: [Category] = category_service.get_categories_by_freelance_site(freelance_site)
        subscriptions: [Subcategory] = subcategory_service.get_subcategories_of_chat(chat)

        count_of_subcategories: int = 0
        count_founded_subs: int = 0

        for c in categories:
            subcategories: [Subcategory] = subcategory_service.get_subcategories_by_category_id(c.id)
            for sub in subcategories:
                count_of_subcategories += 1
                if sub.id in [subscription.id for subscription in subscriptions]:
                    count_founded_subs += 1

        if count_founded_subs == count_of_subcategories:
            markup.add(telebot.types.InlineKeyboardButton(text=freelance_site.value + " ✅",
                                                          callback_data=freelance_site.value))
        elif count_founded_subs == 0:
            markup.add(telebot.types.InlineKeyboardButton(text=freelance_site.value + " ❌",
                                                          callback_data=freelance_site.value))
        else:
            markup.add(telebot.types.InlineKeyboardButton(text=freelance_site.value + " ➖",
                                                          callback_data=freelance_site.value))

    markup.add(telebot.types.InlineKeyboardButton(text="<== Go Back <==",
                                                  callback_data="Back START"))
    for sub_message in SUBS_MESSAGES:
        send_message_to_chat(chat_id=message.chat.id,
                             message=sub_message,
                             reply_markup=markup,
                             parse_mode='HTML')

    chat_service.update_chat_state(message.chat.id, ChatState.SUBS)


def start():
    bot.polling()
