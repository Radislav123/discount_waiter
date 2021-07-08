from telegram_bot_app.telegram_bot.service import *
from service_app.logger import get_logger
import functools
import logging


logger = get_logger(__name__)


def cancel_button_in_callback(callback_function):
    @functools.wraps(callback_function)
    def wrapper(callback, *args, **kwargs):
        callback_data = get_callback_data(callback)
        if callback_data != CANCEL_BUTTON_TEXT_RUS and callback_data != CANCEL_BUTTON_TEXT_EN:
            handler_return = callback_function(callback, *args, **kwargs)
        else:
            bot.clear_step_handler(callback.message)
            handler_return = bot.edit_message_text(
                CANCEL_BUTTON_TEXT_RUS,
                callback.message.chat.id,
                callback.message.id
            )
            logger.log_inside_telegram_command(logging.DEBUG, callback, "cancel button was pressed")
        return handler_return

    return wrapper


def is_callback_handler(command, handler_number = 0):
    def wrapper(callback):
        return True if get_callback_handler_number(callback) == handler_number and callback.data.startswith(command) \
            else False

    return wrapper
