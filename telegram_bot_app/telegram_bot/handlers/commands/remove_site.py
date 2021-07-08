from telegram_bot_app.telegram_bot.handlers.commands.common import *
import logging


logger = get_logger(__name__)


@bot.message_handler(commands = [REMOVE_SITE_COMMAND])
@logger.log_telegram_command(REMOVE_SITE_COMMAND)
def remove_site_command(message):
    """Позволяет убрать сайт из отслеживаемых пользователем."""

    buttons_data = get_discount_hunter_tracked_sites_names(message.chat.id)
    rows = get_inline_button_rows(REMOVE_SITE_COMMAND, buttons_data)
    # в обратный вызов передается название сайта
    reply_markup = get_inline_keyboard_markup(*rows, get_inline_cancel_button_row(REMOVE_SITE_COMMAND))

    if len(rows) > 0:
        bot.send_message(message.chat.id, REMOVE_SITE__CHOOSE_SITE_TEXT, reply_markup = reply_markup)
    else:
        bot.send_message(message.chat.id, REMOVE_SITE__HAVE_NO_SITES_TEXT)


@bot.callback_query_handler(func = is_callback_handler(REMOVE_SITE_COMMAND))
@logger.log_telegram_callback
@cancel_button_in_callback
def remove_site_callback_handler(callback):
    site_name = get_callback_data(callback)
    link = get_discount_hunter_site_link(callback.message.chat.id, site_name)
    link.active = False
    link.save()
    bot.edit_message_text(
        escape_string(REMOVE_SITE__SUCCESS_FINISH_TEMPLATE.format(site_name = site_name, site_url = link.site.address)),
        callback.message.chat.id,
        callback.message.id,
        parse_mode = MARKDOWN_PARSE_MODE,
        disable_web_page_preview = True
    )
    logger.log_inside_telegram_command(
        logging.DEBUG,
        callback,
        f"discount_hunter_site_link for \"{link.site.name}\" site was deactivated"
    )
