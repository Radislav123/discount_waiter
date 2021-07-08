from telegram_bot_app.telegram_bot.handlers.commands.common import *
from django.core.exceptions import ObjectDoesNotExist
import logging


logger = get_logger(__name__)


@bot.message_handler(commands = [START_COMMAND])
@logger.log_telegram_command(START_COMMAND)
def start_command(message):
    """Создает запись о пользователе у бота."""

    # https://stackoverflow.com/a/50522783
    try:
        models.DiscountHunter.objects.filter(
            telegram_chat_id = message.chat.id,
            telegram_user_id = message.from_user.id
        ).get()
        logger.log_inside_telegram_command(logging.DEBUG, message, "discount hunter was found")
    except ObjectDoesNotExist:
        discount_hunter = models.DiscountHunter(
            telegram_chat_id = message.chat.id,
            telegram_user_id = message.from_user.id,
            telegram_username = message.from_user.username,
            telegram_user_first_name = message.from_user.first_name,
            telegram_user_last_name = message.from_user.last_name
        )
        discount_hunter.save()
        logger.log_inside_telegram_command(logging.DEBUG, message, "discount hunter was created")
    bot.send_message(message.chat.id, START__RESPONSE_TEXT)
