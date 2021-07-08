from telegram_bot_app.telegram_bot.handlers.commands.common import *


logger = get_logger(__name__)


@bot.message_handler(commands = [COMMAND_LIST_COMMAND])
@logger.log_telegram_command(COMMAND_LIST_COMMAND)
def command_list_command(message):
    """Выводит список доступных команд."""

    bot.send_message(message.chat.id, get_command_list_text())
