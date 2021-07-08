from telegram_bot_app.telegram_bot.handlers.commands.common import *
from telegram_bot.service.time_related import delayed_task
import logging


logger = get_logger(__name__)


@bot.message_handler(commands = [SITE_CREDENTIALS_COMMAND])
@logger.log_telegram_command(SITE_CREDENTIALS_COMMAND)
def site_credentials_command(message):
    """Временно показывает логин и пароль для отслеживаемого сайта."""

    buttons_data = get_discount_hunter_tracked_sites_names(message.chat.id)
    rows = get_inline_button_rows(SITE_CREDENTIALS_COMMAND, buttons_data)
    # в обратный вызов передается название сайта
    reply_markup = get_inline_keyboard_markup(*rows, get_inline_cancel_button_row(SITE_CREDENTIALS_COMMAND))

    if len(rows) > 0:
        response_text = SITE_CREDENTIALS__CHOOSE_SITE_TEXT
    else:
        response_text = SITE_CREDENTIALS__HAVE_NO_SITES_TEXT

    bot.send_message(message.chat.id, response_text, reply_markup = reply_markup)


@bot.callback_query_handler(func = is_callback_handler(SITE_CREDENTIALS_COMMAND))
@logger.log_telegram_callback
@cancel_button_in_callback
def site_credentials_callback_handler(callback):
    link = get_discount_hunter_site_link(
        callback.message.chat.id,
        get_callback_data(callback)
    )
    message_text = f"логин : {link.login}\nпароль : {link.password}"
    bot.edit_message_text(message_text, callback.message.chat.id, callback.message.id)
    delayed_task(DELETE_SITE_CREDENTIALS_OFFSET, bot.delete_message, callback.message.chat.id, callback.message.id)
    logger.log_inside_telegram_command(
        logging.INFO,
        callback,
        f"site credentials for \"{link.site.name}\" site will be deleted"
        f" from the the chat after {DELETE_SITE_CREDENTIALS_OFFSET} seconds"
    )
