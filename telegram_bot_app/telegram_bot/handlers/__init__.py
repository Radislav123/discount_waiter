# noinspection PyUnresolvedReferences
from telegram_bot_app.telegram_bot.handlers import commands
from telegram_bot_app.telegram_bot.service import *
from service_app.logger import get_logger


logger = get_logger(__name__)


@bot.message_handler(content_types = ["text"])
def unrecognized_messages(message):
    """Дает ответ, если сообщение пользователя не было распознано."""

    bot.send_message(message.chat.id, UNRECOGNIZED_MESSAGE_RESPONSE)
