from telegram_bot_app.telegram_bot.handlers.commands.common import *


logger = get_logger(__name__)


@bot.message_handler(commands = [TRACKED_SITES_COMMAND])
@logger.log_telegram_command(TRACKED_SITES_COMMAND)
def tracked_sites_command(message):
    """Выводит, отслеживаемые пользователем, сайты."""

    links = models.DiscountHunterSiteLink.objects.filter(
        discount_hunter = get_discount_hunter(message.chat.id),
        active = True
    )
    buttons_data = {link.site.name: link.site.url for link in links}
    rows = get_inline_button_rows(TRACKED_SITES_COMMAND, buttons_data, linked = True)

    if len(rows) > 0:
        reply_message = TRACKED_SITES__SUCCESS_RESPONSE_TEXT
    else:
        reply_message = TRACKED_SITES__HAVE_NO_SITES_TEXT
    reply_markup = get_inline_keyboard_markup(*rows)

    bot.send_message(message.chat.id, reply_message, reply_markup = reply_markup, disable_web_page_preview = True)
