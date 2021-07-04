# noinspection PyUnresolvedReferences
import pep8_e402_import_django
from telegram_bot_app.telegram_bot.service.time_related import *
from django.core.exceptions import ObjectDoesNotExist
from telegram_bot_app.telegram_bot.service import *
from service_app.logger import get_logger
from service_app import models
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
            handler_return = bot.edit_message_text(
                CANCEL_BUTTON_TEXT_RUS,
                callback.message.chat.id,
                callback.message.id
            )
            logger.log_inside_telegram_command(logging.INFO, callback, "cancel button was pressed")
        return handler_return

    return wrapper


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
    keys = get_inline_key_rows_from_names(ADD_SITE_COMMAND, site_names, forbidden_names = tracking_sites_names)[0]

    reply_markup = get_inline_keyboard_markup(keys, get_inline_cancel_key(ADD_SITE_COMMAND))
    if len(keys) > 0:
        send_message_return = bot.send_message(
            message.chat.id,
            ADD_SITE_COMMAND_RESPONSE_TEXT,
            reply_markup = reply_markup
        )
    else:
        send_message_return = bot.send_message(
            message.chat.id,
            ADD_SITE_COMMAND_RESPONSE_TEXT_1
        )
    # в обратный вызов передается название сайта
    return send_message_return


@bot.callback_query_handler(func = lambda callback: callback.data.startswith(ADD_SITE_COMMAND))
@logger.log_telegram_callback
@cancel_button_in_callback
def add_site_callback_handler(callback):
    discount_hunter = get_discount_hunter_by_chat_id(callback.message.chat.id)
    tracking_site = get_tracking_site_by_name(get_callback_data(callback))
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
    bot.register_next_step_handler(
        callback.message,
        add_site_get_login_step,
        callback.message,
        link,
        not link.active
    )
    logger.log_inside_telegram_command(
        logging.INFO,
        callback,
        f"user login was requested for \"{link.site.name}\" site"
    )


@logger.log_telegram_callback
def add_site_get_login_step(user_message, bot_message, link, update):
    link.login = user_message.text
    bot.delete_message(user_message.chat.id, user_message.id)
    bot.edit_message_text(
        ADD_SITE_REQUEST_PASSWORD_TEMPLATE.format(site_name = link.site.name),
        bot_message.chat.id,
        bot_message.id
    )
    bot.register_next_step_handler(
        user_message,
        add_site_get_password_step,
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
def add_site_get_password_step(user_message, bot_message, link, update):
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


# noinspection DuplicatedCode
@bot.message_handler(commands = [REMOVE_SITE_COMMAND])
@logger.log_telegram_command(REMOVE_SITE_COMMAND)
def remove_site_command(message):
    """Позволяет убрать сайт из отслеживаемых пользователем."""

    tracking_sites_names = get_discount_hunter_tracking_sites_names(message.chat.id)
    keys = get_inline_key_rows_from_names(REMOVE_SITE_COMMAND, tracking_sites_names)[0]

    reply_markup = get_inline_keyboard_markup(keys, get_inline_cancel_key(REMOVE_SITE_COMMAND))
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
    # в обратный вызов передается название сайта
    return send_message_return


@bot.callback_query_handler(func = lambda callback: callback.data.startswith(REMOVE_SITE_COMMAND))
@logger.log_telegram_callback
@cancel_button_in_callback
def remove_site_callback_handler(callback):
    site_name = get_callback_data(callback)
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
    return handler_return


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


@bot.message_handler(commands = [SITE_CREDENTIALS_COMMAND])
@logger.log_telegram_command(SITE_CREDENTIALS_COMMAND)
def site_credentials_command(message):
    """Временно показывает логин и пароль для отслеживаемого сайта."""

    tracking_sites_names = get_discount_hunter_tracking_sites_names(message.chat.id)
    keys = get_inline_key_rows_from_names(SITE_CREDENTIALS_COMMAND, tracking_sites_names)[0]

    reply_markup = get_inline_keyboard_markup(keys, get_inline_cancel_key(SITE_CREDENTIALS_COMMAND))
    if len(keys) > 0:
        response_text = SITE_CREDENTIALS_COMMAND_RESPONSE_TEXT
    else:
        response_text = SITE_CREDENTIALS_COMMAND_RESPONSE_TEXT_1
    # в обратный вызов передается название сайта
    return bot.send_message(message.chat.id, response_text, reply_markup = reply_markup)


@bot.callback_query_handler(func = lambda callback: callback.data.startswith(SITE_CREDENTIALS_COMMAND))
@logger.log_telegram_callback
@cancel_button_in_callback
def site_credentials_callback_handler(callback):
    link = get_discount_hunter_site_link_by_chat_id_and_site_name(
        callback.message.chat.id,
        get_callback_data(callback)
    )
    message_text = f"логин : {link.login}\nпароль : {link.password}"
    handler_return = bot.edit_message_text(message_text, callback.message.chat.id, callback.message.id)
    delayed_task(DELETE_SITE_CREDENTIALS_OFFSET, bot.delete_message, callback.message.chat.id, callback.message.id)
    logger.log_inside_telegram_command(
        logging.INFO,
        callback,
        f"site credentials for \"{link.site.name}\" site will be deleted after {DELETE_SITE_CREDENTIALS_OFFSET} seconds"
    )
    return handler_return


# noinspection DuplicatedCode
@bot.message_handler(commands = [ADD_CLOTHES_COMMAND])
@logger.log_telegram_command(ADD_CLOTHES_COMMAND)
def add_clothes_command(message):
    """Позволяет добавить элемент одежды для отслеживания."""

    # выбор сайта, на котором найдена вещь
    tracking_sites_names = get_discount_hunter_tracking_sites_names(message.chat.id)
    keys = get_inline_key_rows_from_names(ADD_CLOTHES_COMMAND, tracking_sites_names)[0]

    reply_markup = get_inline_keyboard_markup(keys, get_inline_cancel_key(ADD_CLOTHES_COMMAND))
    if len(keys) > 0:
        send_message_return = bot.send_message(
            message.chat.id,
            ADD_CLOTHES_COMMAND_RESPONSE_TEXT,
            reply_markup = reply_markup
        )
    else:
        send_message_return = bot.send_message(
            message.chat.id,
            ADD_CLOTHES_COMMAND_RESPONSE_TEXT_1
        )
    # в обратный вызов передается название сайта
    return send_message_return


def is_first_add_clothes_callback_handler(callback):
    return True if get_callback_handler_number(callback) == 0 and callback.data.startswith(ADD_CLOTHES_COMMAND) \
        else False


def is_second_add_clothes_callback_handler(callback):
    return True if get_callback_handler_number(callback) == 1 and callback.data.startswith(ADD_CLOTHES_COMMAND) \
        else False


def is_third_add_clothes_callback_handler(callback):
    return True if get_callback_handler_number(callback) == 2 and callback.data.startswith(ADD_CLOTHES_COMMAND) \
        else False


@bot.callback_query_handler(func = is_first_add_clothes_callback_handler)
@logger.log_telegram_callback
@cancel_button_in_callback
def add_clothes_callback_handler(callback):
    # в extras передается id инстанса TrackingSite
    key_extras = models.TrackingSite.objects.get(name = get_callback_data(callback)).id
    # выбор типа элемента одежды
    next_handler_number = 1
    rows = get_inline_key_rows_from_names(
        ADD_CLOTHES_COMMAND,
        models.ClothesType.rus_to_en,
        keys_in_row = 2,
        handler_number = next_handler_number,
        extras = key_extras
    )

    reply_markup = get_inline_keyboard_markup(
        *rows,
        get_inline_cancel_key(ADD_CLOTHES_COMMAND, handler_number = next_handler_number, extras = key_extras)
    )
    bot.edit_message_text(
        ADD_CLOTHES_COMMAND_RESPONSE_TEXT_2,
        callback.message.chat.id,
        callback.message.id,
        reply_markup = reply_markup
    )


@bot.callback_query_handler(func = is_second_add_clothes_callback_handler)
@logger.log_telegram_callback
@cancel_button_in_callback
def add_clothes_callback_handler_1(callback):
    # запрос на ввод ссылки на элемент одежды
    bot.edit_message_text(
        ADD_CLOTHES_REQUEST_CLOTHES_URL_TEXT,
        callback.message.chat.id,
        callback.message.id
    )
    bot.register_next_step_handler(
        callback.message,
        add_clothes_get_clothes_url_step,
        callback.message,
        models.TrackingSite.objects.get(id = get_callback_extras(callback)),
        models.ClothesType.objects.get(name = get_callback_data(callback))
    )


@logger.log_telegram_callback
def add_clothes_get_clothes_url_step(user_message, bot_message, site, clothes_type):

    # в extras передается id инстанса Clothes
    clothes = models.Clothes(
        discount_hunter_site_link = get_discount_hunter_site_link_by_chat_id_and_site_name(
            bot_message.chat.id,
            site.name
        ),
        type = clothes_type,
        url = user_message.text
    )
    # тут нужно получить с сайта размеры одежды и дать выбрать пользователю
    # todo: rewrite sizes detection with scrapy (должен дописывать в поле sizes_on_site)
    sizes = ["S", "L", "XL"]
    clothes.save()
    key_extras = clothes.id

    next_handler_number = 2
    # выбор размеров
    rows = get_inline_key_rows_from_names(
        ADD_CLOTHES_COMMAND,
        clothes.sizes_on_site,
        handler_number = next_handler_number,
        extras = key_extras
    )
    keyboard_markup = get_inline_keyboard_markup(
        *rows,
        get_inline_finish_key(ADD_CLOTHES_COMMAND, next_handler_number, key_extras)
    )

    bot.edit_message_text(
        ADD_CLOTHES_REQUEST_CLOTHES_SIZE_TEXT,
        bot_message.chat.id,
        bot_message.id,
        reply_markup = keyboard_markup
    )


def get_button_names_for_sizes(clothes, remove_size_callback_prefix):
    names = {x: x for x in clothes.sizes_on_site}
    if clothes.sizes is not None:
        for size in clothes.sizes:
            del names[size]
            names.update({f"убрать {size}": f"{remove_size_callback_prefix}{size}"})
    return names


# todo: write remove_clothes_command
# todo: write add_clothes_sizes_command
# todo: write remove_clothes_sizes_command
# todo: write add_default_clothes_sizes_command
# todo: write remove_default_clothes_sizes_command
@bot.callback_query_handler(func = is_third_add_clothes_callback_handler)
@logger.log_telegram_callback
def add_clothes_callback_handler_2(callback):
    callback_data = get_callback_data(callback)
    callback_extras = get_callback_extras(callback)
    clothes = models.Clothes.objects.get(id = int(callback_extras))
    remove_size_callback_prefix = "remove-"

    if callback_data == FINISH_BUTTON_TEXT_EN:
        bot.edit_message_text(
            ADD_CLOTHES_COMMAND_FINISH_TEMPLATE.format(clothes_url = clothes.url, sizes = clothes.sizes_to_order)
        )
    else:
        if callback_data.startswith(remove_size_callback_prefix):
            clothes.sizes.remove(callback_data)
            clothes.save()
            logger.log_inside_telegram_command(
                logging.INFO,
                callback,
                f"\"{callback_data}\" size was removed for {clothes.discount_hunter_site_link.site.name} site"
                f" and clothes with url - ({clothes.url})."
            )
        else:
            clothes.sizes.append(callback_data)
            clothes.save()
            logger.log_inside_telegram_command(
                logging.INFO,
                callback,
                f"\"{callback_data}\" size was added for {clothes.discount_hunter_site_link.site.name} site"
                f" and clothes with url - ({clothes.url})."
            )

        next_handler_number = get_callback_handler_number(callback)
        buttons_names = get_button_names_for_sizes(clothes, remove_size_callback_prefix)
        rows = get_inline_key_rows_from_names(
            ADD_CLOTHES_COMMAND,
            buttons_names,
            handler_number = next_handler_number,
            extras = callback_extras
        )
        keyboard_markup = get_inline_keyboard_markup(
            *rows,
            get_inline_finish_key(ADD_CLOTHES_COMMAND, next_handler_number, callback_extras)
        )
        bot.edit_message_text(
            ADD_CLOTHES_REQUEST_CLOTHES_SIZE_TEXT,
            callback.message.chat.id,
            callback.message,
            reply_markup = keyboard_markup
        )


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
