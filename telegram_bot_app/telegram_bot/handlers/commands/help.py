from telegram_bot_app.telegram_bot.handlers.commands.common import *


logger = get_logger(__name__)


@bot.message_handler(commands = [HELP_COMMAND])
@logger.log_telegram_command(HELP_COMMAND)
def help_command(message):
    """Выводит информацию о боте."""

    bot.send_message(message.chat.id, BOT_DESCRIPTION)
