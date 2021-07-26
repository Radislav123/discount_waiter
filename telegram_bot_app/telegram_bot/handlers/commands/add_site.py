from telegram_bot_app.telegram_bot.handlers.commands.common import *
from service_app.service import update_model_instance
import logging


logger = get_logger(__name__)


@bot.message_handler(commands = [ADD_SITE_COMMAND])
@logger.log_telegram_command(ADD_SITE_COMMAND)
def add_site_command(message):
    """Дает возможность пользователю добавить сайт для отслеживания."""

    tracking_sites_names = get_discount_hunter_tracked_sites_names(message.chat.id)
    buttons_data = [site.name for site in models.Site.objects.all()]
    # в обратный вызов передается название сайта
    rows = get_inline_button_rows(ADD_SITE_COMMAND, buttons_data, forbidden_button_texts = tracking_sites_names)
    reply_markup = get_inline_keyboard_markup(*rows, get_inline_cancel_button_row(ADD_SITE_COMMAND))

    if len(rows) > 0:
        bot.send_message(message.chat.id, ADD_SITE__CHOOSE_SITE_TEXT, reply_markup = reply_markup)
    else:
        bot.send_message(message.chat.id, ADD_SITE__HAVE_NO_SITES_TO_ADD_TEXT)


@bot.callback_query_handler(func = is_callback_handler(ADD_SITE_COMMAND))
@logger.log_telegram_callback
@cancel_button_in_callback
def add_site_callback_handler(callback):
    discount_hunter = get_discount_hunter(callback.message.chat.id)
    tracking_site = get_tracked_site(get_callback_data(callback))
    if models.DiscountHunterSiteLink.objects.filter(
            discount_hunter = discount_hunter,
            site = tracking_site,
            # todo: add handler to set shop_address and shop_city
            shop_city = "default",
            shop_address = "default"
    ).count() == 0:
        link = models.DiscountHunterSiteLink(
            discount_hunter = discount_hunter,
            site = tracking_site,
            active = True
        )
    else:
        link = get_discount_hunter_site_link(callback.message.chat.id, tracking_site.name)
        link.active = True

    bot.edit_message_text(
        escape_string(ADD_SITE__INPUT_LOGIN_TEMPLATE.format(site_name = link.site.name, site_url = link.site.url)),
        callback.message.chat.id,
        callback.message.id,
        parse_mode = MARKDOWN_PARSE_MODE,
        disable_web_page_preview = True
    )
    bot.register_next_step_handler(callback.message, add_site_get_login_step, callback.message, link, not link.active)
    logger.log_inside_telegram_command(
        logging.DEBUG,
        callback,
        f"user login was requested for \"{link.site.name}\" site"
    )


@logger.log_telegram_callback
def add_site_get_login_step(user_message, bot_message, link, update):
    link.login = user_message.text
    bot.delete_message(user_message.chat.id, user_message.id)
    bot.edit_message_text(
        escape_string(
            ADD_SITE__INPUT_PASSWORD_TEMPLATE.format(site_name = link.site.name, site_url = link.site.url)
        ),
        bot_message.chat.id,
        bot_message.id,
        parse_mode = MARKDOWN_PARSE_MODE,
        disable_web_page_preview = True
    )
    bot.register_next_step_handler(user_message, add_site_get_password_step, bot_message, link, update)
    logger.log_inside_telegram_command(
        logging.DEBUG,
        user_message,
        f"user password was requested for \"{link.site.name}\" site"
    )


@logger.log_telegram_callback
def add_site_get_password_step(user_message, bot_message, link, update):
    link.password = user_message.text
    if not update:
        link.save()
        logger.log_inside_telegram_command(
            logging.DEBUG,
            user_message,
            f"discount_hunter_site_link for \"{link.site.name}\" site was saved"
        )
    else:
        filters = {
            "discount_hunter": get_discount_hunter(user_message.chat.id),
            "site": get_tracked_site(link.site.name)
        }
        update_model_instance(models.DiscountHunterSiteLink, link, filters)
        logger.log_inside_telegram_command(
            logging.DEBUG,
            user_message,
            f"discount_hunter_site_link for \"{link.site.name}\" site was updated"
        )
    bot.delete_message(user_message.chat.id, user_message.id)

    bot.edit_message_text(
        escape_string(
            ADD_SITE__SUCCESS_FINISH_TEMPLATE.format(site_name = link.site.name, site_url = link.site.url)
        ),
        bot_message.chat.id,
        bot_message.id,
        parse_mode = MARKDOWN_PARSE_MODE,
        disable_web_page_preview = True
    )
