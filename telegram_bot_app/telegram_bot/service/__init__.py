# noinspection PyUnresolvedReferences
import pep8_e402_import_django
from telegram_bot_app.telegram_bot.constants import *
from discount_waiter.settings import BASE_DIR
from secure.telegram_bot import API_TOKEN
from service_app import models
import platform
# noinspection PyPackageRequirements
import telebot
import re


bot = telebot.TeleBot(API_TOKEN)
commands = []


def get_platform():
    return platform.node()


def get_command_list_text():
    text = ""
    for command, description in get_commands_with_descriptions():
        text += '/' + command + "   " + description + '\n'
    return text


def get_commands_with_descriptions():
    if len(commands) == 0:
        commands_path = f"{BASE_DIR}/telegram_bot_app/telegram_bot/commands.py"
        with open(commands_path, encoding = "utf-8") as command_file:
            for line in command_file:
                if line == '\n':
                    pair = [command_file.readline().split(" = ")[1], command_file.readline().split(" = ")[1]]
                    pair[0] = pair[0][1:-2]
                    pair[1] = pair[1][1:-2]
                    commands.append(pair)
    return commands


def set_bot_command_list():
    bot_commands = []
    for pair in get_commands_with_descriptions():
        bot_commands.append(telebot.types.BotCommand(pair[0], pair[1]))
    return bot.set_my_commands(bot_commands)


def get_keyboard_markup(rows):
    """Возвращает готовую разметку кнопок."""

    # rows должен быть типа [[telebot.types.InlineKeyboardButton,..],..]
    keyboard_markup = telebot.types.InlineKeyboardMarkup()
    for keys in rows:
        keyboard_markup.row(*keys)
    return keyboard_markup


def get_keyboard_markup_with_cancel_button(rows, cancel_button_callback_data):
    """Как get_keyboard_markup, только последней строкой добавляет кнопку отмены."""

    rows = list(rows)
    rows.append(
        [
            telebot.types.InlineKeyboardButton(
                text = CANCEL_BUTTON_TEXT,
                callback_data = cancel_button_callback_data
            )
        ]
    )
    return get_keyboard_markup(rows)


def get_callback_data(callback):
    return re.findall(CALLBACK_REGEX_TEMPLATE, callback.data)[0][2]


def get_discount_hunter_tracking_sites_names(chat_id):
    site_links = models.DiscountHunterSiteLink.objects.filter(
        discount_hunter = models.DiscountHunter.objects.get(telegram_chat_id = chat_id)
    )
    return [link.site.name for link in site_links if link.active]


def get_key_row_from_names(command, names, forbidden_names = ()):
    keys = []
    for name in names:
        if name not in forbidden_names:
            keys.append(
                telebot.types.InlineKeyboardButton(
                    text = name,
                    callback_data = CALLBACK_DATA_TEMPLATE.format(command = command, data = name)
                )
            )
    return keys


def update_model_instance(model, model_instance, filters):
    update_data = model_instance.__dict__.copy()
    del update_data["_state"]
    del update_data["id"]
    return model.objects.filter(**filters).update(**update_data)


def get_discount_hunter_by_chat_id(chat_id):
    return models.DiscountHunter.objects.get(telegram_chat_id = chat_id)


def get_tracking_site_by_name(site_name):
    return models.TrackingSite.objects.get(name = site_name)


def get_discount_hunter_site_link_by_chat_id_and_site_name(chat_id, site_name):
    return models.DiscountHunterSiteLink.objects.get(
        discount_hunter = get_discount_hunter_by_chat_id(chat_id),
        site = get_tracking_site_by_name(site_name)
    )
