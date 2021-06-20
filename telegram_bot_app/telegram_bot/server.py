# noinspection PyUnresolvedReferences
import pep8_e402_import_django
from telegram_bot_app.telegram_bot.service.time_related import *
from django.core.exceptions import ObjectDoesNotExist
from telegram_bot_app.telegram_bot.service import *
from service_app.logger import get_logger
from service_app import models
import logging


logger = get_logger(__name__)


@bot.callback_query_handler(func = lambda callback: callback.data.startswith(ADD_SITE_COMMAND))
@logger.log_telegram_callback
def add_site_callback_handler(callback):
    callback_data = get_callback_data(callback)
    discount_hunter = get_discount_hunter_by_chat_id(callback.message.chat.id)
    if callback_data != CANCEL_BUTTON_TEXT:
        tracking_site = get_tracking_site_by_name(callback_data)
        if models.DiscountHunterSiteLink.objects.filter(
                discount_hunter = discount_hunter,
                site = tracking_site
        ).count() == 0:
            link = models.DiscountHunterSiteLink(
                discount_hunter = discount_hunter,
                site = tracking_site,
                active = True
            )
        else:
            link = get_discount_hunter_site_link_by_chat_id_and_site_name(callback.message.chat.id, tracking_site.name)
            link.active = True

        bot.edit_message_text(
            ADD_SITE_REQUEST_LOGIN_TEMPLATE.format(site_name = link.site.name),
            callback.message.chat.id,
            callback.message.id
        )
        handler_return = bot.register_next_step_handler(
            callback.message,
            add_site_request_login_step,
            callback.message,
            link,
            not link.active
        )
        logger.log_inside_telegram_command(
            logging.INFO,
            callback,
            f"user login was requested for \"{link.site.name}\" site"
        )
    else:
        handler_return = bot.edit_message_text(CANCEL_BUTTON_TEXT, callback.message.chat.id, callback.message.id)
        logger.log_inside_telegram_command(logging.INFO, callback, "cancel button was pressed")
    return handler_return


@logger.log_telegram_callback
def add_site_request_login_step(user_message, bot_message, link, update):
    link.login = user_message.text
    bot.delete_message(user_message.chat.id, user_message.id)
    bot.edit_message_text(
        ADD_SITE_REQUEST_PASSWORD_TEMPLATE.format(site_name = link.site.name),
        bot_message.chat.id,
        bot_message.id
    )
    bot.register_next_step_handler(
        user_message,
        add_site_request_password_step,
        bot_message,
        link,
        update
    )
    logger.log_inside_telegram_command(
        logging.INFO,
        user_message,
        f"user password was requested for \"{link.site.name}\" site"
    )


@logger.log_telegram_callback
def add_site_request_password_step(user_message, bot_message, link, update):
    link.password = user_message.text
    if not update:
        link.save()
        logger.log_inside_telegram_command(
            logging.INFO,
            user_message,
            f"discount_hunter_site_link for \"{link.site.name}\" site was saved"
        )
    else:
        filters = {
            "discount_hunter": get_discount_hunter_by_chat_id(user_message.chat.id),
            "site": get_tracking_site_by_name(link.site.name)
        }
        update_model_instance(models.DiscountHunterSiteLink, link, filters)
        logger.log_inside_telegram_command(
            logging.INFO,
            user_message,
            f"discount_hunter_site_link for \"{link.site.name}\" site was updated"
        )
    bot.delete_message(user_message.chat.id, user_message.id)
    return bot.edit_message_text(
        ADD_SITE_SUCCESS_RESPONSE_TEXT,
        bot_message.chat.id,
        bot_message.id
    )


@bot.callback_query_handler(func = lambda callback: callback.data.startswith(REMOVE_SITE_COMMAND))
@logger.log_telegram_callback
def remove_site_callback_handler(callback):
    callback_data = get_callback_data(callback)
    if callback_data != CANCEL_BUTTON_TEXT:
        site_name = callback_data
        link = get_discount_hunter_site_link_by_chat_id_and_site_name(callback.message.chat.id, site_name)
        link.active = False
        link.save()
        handler_return = bot.edit_message_text(
            REMOVE_SITE_SUCCESS_RESPONSE_TEMPLATE.format(site_name = site_name),
            callback.message.chat.id,
            callback.message.id
        )
        logger.log_inside_telegram_command(
            logging.INFO,
            callback,
            f"discount_hunter_site_link for \"{link.site.name}\" site was deactivated"
        )
    else:
        handler_return = bot.edit_message_text(CANCEL_BUTTON_TEXT, callback.message.chat.id, callback.message.id)
        logger.log_inside_telegram_command(logging.INFO, callback, "cancel button was pressed")
    return handler_return


@bot.callback_query_handler(func = lambda callback: callback.data.startswith(SITE_CREDENTIALS))
@logger.log_telegram_callback
def site_credentials_callback_handler(callback):
    link = get_discount_hunter_site_link_by_chat_id_and_site_name(callback.message.chat.id, get_callback_data(callback))
    message_text = f"логин : {link.login}\nпароль : {link.password}"
    edit_message_return = bot.edit_message_text(message_text, callback.message.chat.id, callback.message.id)
    delayed_task(60, bot.delete_message, callback.message.chat.id, callback.message.id)
    logger.log_inside_telegram_command(
        logging.INFO,
        callback,
        f"site credentials for \"{link.site.name}\" site will be deleted after 60  seconds"
    )
    return edit_message_return


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
        logger.log_inside_telegram_command(logging.INFO, message, "discount hunter was found")
    except ObjectDoesNotExist:
        discount_hunter = models.DiscountHunter(
            telegram_chat_id = message.chat.id,
            telegram_user_id = message.from_user.id,
            telegram_username = message.from_user.username,
            telegram_user_first_name = message.from_user.first_name,
            telegram_user_last_name = message.from_user.last_name
        )
        discount_hunter.save()
        logger.log_inside_telegram_command(logging.INFO, message, "discount hunter was created")
    return bot.send_message(message.chat.id, START_COMMAND_RESPONSE_TEXT)


@bot.message_handler(commands = [ADD_SITE_COMMAND])
@logger.log_telegram_command(ADD_SITE_COMMAND)
def add_site_command(message):
    """Дает возможность пользователю добавить сайт для отслеживания."""

    tracking_sites_names = get_discount_hunter_tracking_sites_names(message.chat.id)
    site_names = [site.name for site in models.TrackingSite.objects.all()]
    keys = get_key_row_from_names(ADD_SITE_COMMAND, site_names, tracking_sites_names)

    keyboard_markup = get_keyboard_markup_with_cancel_button(
        [keys],
        CALLBACK_DATA_CANCEL_TEMPLATE.format(command = ADD_SITE_COMMAND)
    )
    if len(keys) > 0:
        send_message_return = bot.send_message(
            message.chat.id,
            ADD_SITE_COMMAND_RESPONSE_TEXT,
            reply_markup = keyboard_markup
        )
    else:
        send_message_return = bot.send_message(
            message.chat.id,
            ADD_SITE_COMMAND_RESPONSE_TEXT_1
        )
    # в обратный вызов передается имя сайта
    return send_message_return


@bot.message_handler(commands = [REMOVE_SITE_COMMAND])
@logger.log_telegram_command(REMOVE_SITE_COMMAND)
def remove_site_command(message):
    """Позволяет убрать сайт из отслеживаемых пользователем."""

    tracking_sites_names = get_discount_hunter_tracking_sites_names(message.chat.id)
    keys = get_key_row_from_names(REMOVE_SITE_COMMAND, tracking_sites_names)
    reply_markup = get_keyboard_markup_with_cancel_button(
        [keys],
        CALLBACK_DATA_CANCEL_TEMPLATE.format(command = REMOVE_SITE_COMMAND)
    )
    if len(keys) > 0:
        send_message_return = bot.send_message(
            message.chat.id,
            REMOVE_SITE_COMMAND_RESPONSE_TEXT,
            reply_markup = reply_markup
        )
    else:
        send_message_return = bot.send_message(
            message.chat.id,
            REMOVE_SITE_COMMAND_RESPONSE_TEXT_1
        )
    # в обратный вызов передается имя сайта
    return send_message_return


@bot.message_handler(commands = [TRACKED_SITES_COMMAND])
@logger.log_telegram_command(TRACKED_SITES_COMMAND)
def get_sites_command(message):
    """Выводит, отслеживаемые пользователем, сайты."""

    links = models.DiscountHunterSiteLink.objects.filter(
        discount_hunter = get_discount_hunter_by_chat_id(message.chat.id),
        active = True
    )
    if links.count() > 0:
        reply_message = GET_SITES_COMMAND_RESPONSE_TEXT
        for link in links:
            reply_message += f"{link.site.name} : {link.site.address}\n"
    else:
        reply_message = GET_SITES_COMMAND_RESPONSE_TEXT_1
    return bot.send_message(message.chat.id, reply_message)


@bot.message_handler(commands = [SITE_CREDENTIALS])
@logger.log_telegram_command(SITE_CREDENTIALS)
def site_credentials(message):
    """Временно показывает логин и пароль для отслеживаемого сайта."""

    tracking_sites_names = get_discount_hunter_tracking_sites_names(message.chat.id)
    keys = get_key_row_from_names(SITE_CREDENTIALS, tracking_sites_names)
    reply_markup = get_keyboard_markup([keys])
    if len(keys) > 0:
        response_text = SITE_CREDENTIALS_RESPONSE_TEXT
    else:
        response_text = SITE_CREDENTIALS_RESPONSE_TEXT_1
    # в обратный вызов передается имя сайта
    return bot.send_message(message.chat.id, response_text, reply_markup = reply_markup)


@bot.message_handler(commands = [HELP_COMMAND])
@logger.log_telegram_command(HELP_COMMAND)
def help_command(message):
    """Выводит информацию о боте."""

    return bot.send_message(message.chat.id, BOT_DESCRIPTION)


@bot.message_handler(commands = [COMMAND_LIST_COMMAND])
@logger.log_telegram_command(COMMAND_LIST_COMMAND)
def command_list_command(message):
    """Выводит список доступных команд."""

    return bot.send_message(message.chat.id, get_command_list_text())


@bot.message_handler(content_types = ["text"])
def unrecognized_messages(message):
    """Дает ответ, если сообщение пользователя не было распознано."""

    return bot.send_message(message.chat.id, UNRECOGNIZED_MESSAGE_RESPONSE)


if __name__ == '__main__':
    set_bot_command_list()
    logger.info("bot command list was sent")

    try:
        logger.info("telegram bot was started")

        # уровень info в консоль не пишется, но видеть, что бот запустился, хочется и в консоли
        local_machine_text = "running on the local machine"
        logger.info(local_machine_text)
        print(local_machine_text)

        bot.polling(none_stop = True)
    finally:
        logger.info("telegram bot was stopped\n")
