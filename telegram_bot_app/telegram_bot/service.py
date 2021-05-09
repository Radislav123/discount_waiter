from secure.telegram_bot import API_TOKEN
from discount_waiter.settings import BASE_DIR
import platform
# noinspection PyPackageRequirements
import telebot


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


def get_keyboard_markup(*keys):
    keyboard_markup = telebot.types.InlineKeyboardMarkup()
    keyboard_markup.add(*keys)
    return keyboard_markup
