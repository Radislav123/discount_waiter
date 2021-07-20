# noinspection PyUnresolvedReferences
import pep8_e402_import_django
from telegram_bot_app.telegram_bot.constants import *
from discount_waiter.settings import BASE_DIR
from secure.telegram_bot import API_TOKEN
from service_app import models
# noinspection PyPackageRequirements
import telebot
import json
import re


bot = telebot.TeleBot(API_TOKEN)
commands = []


# для параметра parse_mode = "MarkdownV2" в сообщениях Телеграмм-бота
def escape_string(string):
    escape_characters = ['/', '.', '_', '-', '=']
    for character in escape_characters:
        string = string.replace(character, f"\\{character}")
    return string


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


# если buttons_data словарь, то ключи воспринимаются как названия (текст для кнопок),
# а значения как callback_data или url
# ключи - текст на кнопке
# значения - данные в обратном вызове или ссылки, если linked == True
def get_inline_button_rows(
        command,
        buttons_data,
        forbidden_button_texts = (),
        buttons_in_row = 3,
        handler_number = 0,
        extras = None,
        linked = False
):
    buttons = []
    if type(buttons_data) is list:
        buttons_data = {x: x for x in buttons_data}
    for name in buttons_data:
        if name not in forbidden_button_texts:
            if linked:
                buttons.append(
                    telebot.types.InlineKeyboardButton(
                        text = name,
                        url = buttons_data[name]
                    )
                )
            else:
                buttons.append(
                    telebot.types.InlineKeyboardButton(
                        text = name,
                        callback_data = CALLBACK_DATA_TEMPLATE.format(
                            command = command,
                            handler_number = handler_number,
                            data = buttons_data[name],
                            extras = extras if extras else {}
                        )
                    )
                )

    rows = []
    for i in range((len(buttons) // buttons_in_row)):
        rows.append(buttons[i * buttons_in_row: i * buttons_in_row + buttons_in_row])
    if len(buttons) % buttons_in_row:
        rows.append(buttons[len(buttons) // buttons_in_row * buttons_in_row:])
    return rows


def get_inline_button_rows_with_cancel(
        command,
        buttons_data,
        forbidden_button_texts = (),
        buttons_in_row = 3,
        handler_number = 0,
        extras = None,
        linked = False
):
    rows = get_inline_button_rows(
        command,
        buttons_data,
        forbidden_button_texts,
        buttons_in_row,
        handler_number,
        extras,
        linked
    )
    return [*rows, get_inline_cancel_button_row(command, handler_number = handler_number, extras = extras)]


def get_inline_button_rows_with_finish(
        command,
        buttons_data,
        forbidden_button_texts = (),
        buttons_in_row = 3,
        handler_number = 0,
        extras = None,
        linked = False
):
    rows = get_inline_button_rows(
        command,
        buttons_data,
        forbidden_button_texts,
        buttons_in_row,
        handler_number,
        extras,
        linked
    )
    return [*rows, get_inline_finish_button_row(command, handler_number = handler_number, extras = extras)]


def get_inline_special_button_row(button_text, callback_data_template, command, handler_number = 0, extras = None):
    return [
        telebot.types.InlineKeyboardButton(
            text = button_text,
            callback_data = callback_data_template.format(
                command = command,
                handler_number = handler_number,
                extras = extras if extras else {}
            )
        )
    ]


def get_inline_cancel_button_row(command, button_text = CANCEL_BUTTON_TEXT_RUS, handler_number = 0, extras = None):
    return get_inline_special_button_row(
        button_text,
        CALLBACK_DATA_CANCEL_BUTTON_TEMPLATE,
        command,
        handler_number,
        extras
    )


def get_inline_finish_button_row(command, button_text = FINISH_BUTTON_TEXT_RUS, handler_number = 0, extras = None):
    return get_inline_special_button_row(
        button_text,
        CALLBACK_DATA_FINISH_BUTTON_TEMPLATE,
        command,
        handler_number,
        extras
    )


def get_inline_return_button_row(command, button_text = RETURN_BUTTON_TEXT_RUS, handler_number = 0, extras = None):
    return get_inline_special_button_row(
        button_text,
        CALLBACK_DATA_RETURN_BUTTON_TEMPLATE,
        command,
        handler_number,
        extras
    )


def get_inline_next_button_row(command, button_text = NEXT_BUTTON_TEXT_RUS, handler_number = 0, extras = None):
    return get_inline_special_button_row(
        button_text,
        CALLBACK_DATA_NEXT_BUTTON_TEMPLATE,
        command,
        handler_number,
        extras
    )


def get_inline_keyboard_markup(*rows):
    """Возвращает готовую разметку кнопок."""

    # rows должен быть типа [[telebot.types.InlineKeyboardButton,..],..]
    keyboard_markup = telebot.types.InlineKeyboardMarkup()
    for buttons in rows:
        keyboard_markup.row(*buttons)
    return keyboard_markup


def get_callback_handler_number(callback):
    return int(re.findall(CALLBACK_REGEX_TEMPLATE, callback.data)[0][2])


def get_callback_data(callback):
    return re.findall(CALLBACK_REGEX_TEMPLATE, callback.data)[0][4]


def get_callback_extras(callback):
    return json.loads(re.findall(CALLBACK_REGEX_TEMPLATE, callback.data)[0][6])


def get_discount_hunter_tracked_sites(chat_id):
    return models.DiscountHunterSiteLink.objects.filter(
        discount_hunter = models.DiscountHunter.objects.get(telegram_chat_id = chat_id)
    )


def get_discount_hunter_tracked_sites_names(chat_id):
    return [link.site.name for link in get_discount_hunter_tracked_sites(chat_id) if link.active]


def get_discount_hunter_tracked_items(discount_hunter, site = None, item_type = None):
    if site and item_type:
        tracked_items = models.Item.objects.filter(discount_hunter = discount_hunter, site = site, type = item_type)
    elif site:
        tracked_items = models.Item.objects.filter(discount_hunter = discount_hunter, site = site)
    elif item_type:
        tracked_items = models.Item.objects.filter(discount_hunter = discount_hunter, item_type = item_type)
    else:
        tracked_items = models.Item.objects.filter(discount_hunter = discount_hunter)
    return tracked_items


def get_discount_hunter(chat_id):
    return models.DiscountHunter.objects.get(telegram_chat_id = chat_id)


def get_tracked_site(site_name):
    return models.Site.objects.get(name = site_name)


def get_discount_hunter_site_link(chat_id, site_name):
    return models.DiscountHunterSiteLink.objects.get(
        discount_hunter = get_discount_hunter(chat_id),
        site = get_tracked_site(site_name)
    )
