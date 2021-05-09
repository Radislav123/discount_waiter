from telegram_bot_app.telegram_bot.constants import *
from telegram_bot_app.telegram_bot.commands import *
from telegram_bot_app.telegram_bot.service import *
from service_app.models import DiscountHunter


@bot.message_handler(commands = [START_COMMAND])
def start_command(message):
    # todo: write it
    # https://stackoverflow.com/a/50522783
    person = DiscountHunter(
        telegram_username = message.from_user.username,
        telegram_chat_id = message.chat.id,

    )
    return bot.send_message(message.chat.id, BOT_START_COMMAND_RESPONSE_TEXT)


@bot.message_handler(commands = [HELP_COMMAND])
def help_command(message):
    return bot.send_message(message.chat.id, BOT_DESCRIPTION)


@bot.message_handler(commands = [COMMAND_LIST_COMMAND])
def command_list_command(message):
    return bot.send_message(message.chat.id, get_command_list_text())


@bot.message_handler(content_types = ["text"])
def unrecognized_messages(message):
    return bot.send_message(message.chat.id, UNRECOGNIZED_MESSAGE_RESPONSE)


if __name__ == '__main__':
    set_bot_command_list()
    try:
        print("running on the local machine")
        bot.polling(none_stop = True)
    finally:
        pass
