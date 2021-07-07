# noinspection PyUnresolvedReferences
import pep8_e402_import_django
from scrapers_app.scrapers.zara_item_info_scraper import ZaraItemInfoScraper
from telegram_bot_app.telegram_bot.service.time_related import *
from django.core.exceptions import ObjectDoesNotExist
from telegram_bot_app.telegram_bot.service import *
from django.core.exceptions import ValidationError
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
            bot.clear_step_handler(callback.message)
            handler_return = bot.edit_message_text(
                CANCEL_BUTTON_TEXT_RUS,
                callback.message.chat.id,
                callback.message.id
            )
            logger.log_inside_telegram_command(logging.DEBUG, callback, "cancel button was pressed")
        return handler_return

    return wrapper


def is_numbered_callback_handler(command, handler_number):
    def wrapper(callback):
        return True if get_callback_handler_number(callback) == handler_number and callback.data.startswith(command) \
            else False

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


@bot.message_handler(commands = [ADD_SITE_COMMAND])
@logger.log_telegram_command(ADD_SITE_COMMAND)
def add_site_command(message):
    """Дает возможность пользователю добавить сайт для отслеживания."""

    tracking_sites_names = get_discount_hunter_tracking_sites_names(message.chat.id)
    sites_names = [site.name for site in models.TrackingSite.objects.all()]
    # в обратный вызов передается название сайта
    rows = get_inline_button_rows(ADD_SITE_COMMAND, sites_names, forbidden_button_texts = tracking_sites_names)

    reply_markup = get_inline_keyboard_markup(*rows, get_inline_cancel_button_row(ADD_SITE_COMMAND))
    if len(rows) > 0:
        bot.send_message(message.chat.id, ADD_SITE__CHOOSE_SITE_TEXT, reply_markup = reply_markup)
    else:
        bot.send_message(message.chat.id, ADD_SITE__HAVE_NO_SITES_TO_ADD_TEXT)


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
        ADD_SITE__INPUT_LOGIN_TEMPLATE.format(site_name = link.site.name),
        callback.message.chat.id,
        callback.message.id
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
        ADD_SITE__INPUT_PASSWORD_TEMPLATE.format(site_name = link.site.name),
        bot_message.chat.id,
        bot_message.id
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
            "discount_hunter": get_discount_hunter_by_chat_id(user_message.chat.id),
            "site": get_tracking_site_by_name(link.site.name)
        }
        update_model_instance(models.DiscountHunterSiteLink, link, filters)
        logger.log_inside_telegram_command(
            logging.DEBUG,
            user_message,
            f"discount_hunter_site_link for \"{link.site.name}\" site was updated"
        )
    bot.delete_message(user_message.chat.id, user_message.id)
    bot.edit_message_text(ADD_SITE__SUCCESS_FINISH_TEXT, bot_message.chat.id, bot_message.id)


# noinspection DuplicatedCode
@bot.message_handler(commands = [REMOVE_SITE_COMMAND])
@logger.log_telegram_command(REMOVE_SITE_COMMAND)
def remove_site_command(message):
    """Позволяет убрать сайт из отслеживаемых пользователем."""

    tracking_sites_names = get_discount_hunter_tracking_sites_names(message.chat.id)
    rows = get_inline_button_rows(REMOVE_SITE_COMMAND, tracking_sites_names)
    # в обратный вызов передается название сайта
    reply_markup = get_inline_keyboard_markup(*rows, get_inline_cancel_button_row(REMOVE_SITE_COMMAND))

    if len(rows) > 0:
        bot.send_message(message.chat.id, REMOVE_SITE__CHOOSE_SITE_TEXT, reply_markup = reply_markup)
    else:
        bot.send_message(message.chat.id, REMOVE_SITE__HAVE_NO_SITES_TEXT)


@bot.callback_query_handler(func = lambda callback: callback.data.startswith(REMOVE_SITE_COMMAND))
@logger.log_telegram_callback
@cancel_button_in_callback
def remove_site_callback_handler(callback):
    site_name = get_callback_data(callback)
    link = get_discount_hunter_site_link_by_chat_id_and_site_name(callback.message.chat.id, site_name)
    link.active = False
    link.save()
    bot.edit_message_text(
        REMOVE_SITE__SUCCESS_FINISH_TEMPLATE.format(site_name = site_name),
        callback.message.chat.id,
        callback.message.id
    )
    logger.log_inside_telegram_command(
        logging.DEBUG,
        callback,
        f"discount_hunter_site_link for \"{link.site.name}\" site was deactivated"
    )


@bot.message_handler(commands = [TRACKED_SITES_COMMAND])
@logger.log_telegram_command(TRACKED_SITES_COMMAND)
def get_sites_command(message):
    """Выводит, отслеживаемые пользователем, сайты."""

    links = models.DiscountHunterSiteLink.objects.filter(
        discount_hunter = get_discount_hunter_by_chat_id(message.chat.id),
        active = True
    )
    if links.count() > 0:
        reply_message = TRACKED_SITES__RESPONSE_OK_TEXT
        for link in links:
            reply_message += f"{link.site.name} : {link.site.address}\n"
    else:
        reply_message = TRACKED_SITES__HAVE_NO_SITES_TEXT
    bot.send_message(message.chat.id, reply_message)


@bot.message_handler(commands = [SITE_CREDENTIALS_COMMAND])
@logger.log_telegram_command(SITE_CREDENTIALS_COMMAND)
def site_credentials_command(message):
    """Временно показывает логин и пароль для отслеживаемого сайта."""

    tracking_sites_names = get_discount_hunter_tracking_sites_names(message.chat.id)
    rows = get_inline_button_rows(SITE_CREDENTIALS_COMMAND, tracking_sites_names)
    # в обратный вызов передается название сайта
    reply_markup = get_inline_keyboard_markup(*rows, get_inline_cancel_button_row(SITE_CREDENTIALS_COMMAND))

    if len(rows) > 0:
        response_text = SITE_CREDENTIALS__CHOOSE_SITE_TEXT
    else:
        response_text = SITE_CREDENTIALS__HAVE_NO_SITES_TEXT

    bot.send_message(message.chat.id, response_text, reply_markup = reply_markup)


@bot.callback_query_handler(func = lambda callback: callback.data.startswith(SITE_CREDENTIALS_COMMAND))
@logger.log_telegram_callback
@cancel_button_in_callback
def site_credentials_callback_handler(callback):
    link = get_discount_hunter_site_link_by_chat_id_and_site_name(
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


# noinspection DuplicatedCode
@bot.message_handler(commands = [ADD_ITEM_COMMAND])
@logger.log_telegram_command(ADD_ITEM_COMMAND)
def add_item_command(message):
    """Позволяет добавить вещь для отслеживания."""

    # выбор сайта, на котором найдена вещь
    tracking_sites_names = get_discount_hunter_tracking_sites_names(message.chat.id)
    rows = get_inline_button_rows(ADD_ITEM_COMMAND, tracking_sites_names)
    # в обратный вызов передается название сайта
    reply_markup = get_inline_keyboard_markup(*rows, get_inline_cancel_button_row(ADD_ITEM_COMMAND))

    if len(rows) > 0:
        bot.send_message(message.chat.id, ADD_ITEM__CHOOSE_SITE_OK_TEXT, reply_markup = reply_markup)
    else:
        bot.send_message(message.chat.id, ADD_ITEM__HAVE_NO_SITES_TEXT)


@bot.callback_query_handler(func = is_numbered_callback_handler(ADD_ITEM_COMMAND, 0))
@logger.log_telegram_callback
@cancel_button_in_callback
def add_item_callback_handler(callback):
    """Получение сайта, на котором была найдена вещь."""

    # в extras передается id инстанса TrackingSite
    key_extras = models.TrackingSite.objects.get(name = get_callback_data(callback)).id
    # выбор типа элемента одежды
    next_handler_number = 1
    rows = get_inline_button_rows(
        ADD_ITEM_COMMAND,
        models.ItemType.rus_to_en,
        buttons_in_row = 2,
        handler_number = next_handler_number,
        extras = key_extras
    )

    reply_markup = get_inline_keyboard_markup(
        *rows,
        get_inline_cancel_button_row(ADD_ITEM_COMMAND, handler_number = next_handler_number, extras = key_extras)
    )
    bot.edit_message_text(
        ADD_ITEM__CHOOSE_ITEM_TYPE_TEXT,
        callback.message.chat.id,
        callback.message.id,
        reply_markup = reply_markup
    )


@bot.callback_query_handler(func = is_numbered_callback_handler(ADD_ITEM_COMMAND, 1))
@logger.log_telegram_callback
@cancel_button_in_callback
def add_item_callback_handler_1(callback):
    """Получение типа вещи."""

    # запрос на ввод ссылки на элемент одежды
    bot.edit_message_text(
        ADD_ITEM__INPUT_URL_TEXT,
        callback.message.chat.id,
        callback.message.id,
        reply_markup = get_inline_keyboard_markup(
            get_inline_cancel_button_row(
                ADD_ITEM_COMMAND,
                handler_number = 2,
                # в extras передается id инстанса TrackingSite
                extras = get_callback_extras(callback)
            )
        )
    )
    bot.register_next_step_handler(
        callback.message,
        add_item_get_url_step,
        callback.message,
        models.TrackingSite.objects.get(id = get_callback_extras(callback)),
        models.ItemType.objects.get(name = get_callback_data(callback))
    )


# todo: сделать статистику экономии денег на скидках (и другую статистику)
@logger.log_telegram_callback
def add_item_get_url_step(user_message, bot_message, site, item_type, recursive = False):
    """Получение ссылки на вещь."""

    try:
        item = models.Item(
            discount_hunter_site_link = get_discount_hunter_site_link_by_chat_id_and_site_name(
                bot_message.chat.id,
                site.name
            ),
            type = item_type,
            url = user_message.text,
            sizes = []
        )
        item.validate_url()
        # поля name и sizes_on_site берутся с сайта
        # todo: отвязать от Зары и выбирать из сайтов в базе
        scraper = ZaraItemInfoScraper(item)
        scraper.find_elements_on_page()
        scraper.run()
        item.save()
        # в extras передается id инстанса Item
        key_extras = item.id

        if scraper.found_all_elements:
            next_handler_number = 2
            # выбор размеров
            rows = get_inline_button_rows(
                ADD_ITEM_COMMAND,
                item.sizes_on_site,
                handler_number = next_handler_number,
                extras = key_extras
            )
            reply_markup = get_inline_keyboard_markup(
                *rows,
                get_inline_finish_button_row(ADD_ITEM_COMMAND, next_handler_number, key_extras)
            )
            bot.edit_message_text(
                ADD_ITEM__CHOOSE_SIZES_TEXT,
                bot_message.chat.id,
                bot_message.id,
                reply_markup = reply_markup
            )
        else:
            bot.edit_message_text(ADD_ITEM__NOT_FOUND_INFORMATION_TEXT, bot_message.chat.id, bot_message.id)
            item.delete()
            log_message = f"not found elements ({scraper.not_found_elements})" \
                          f" on the page ({item.url})."
            logger.log_inside_telegram_command(
                logging.INFO,
                user_message,
                log_message
            )
    except ValidationError as error:
        new_bot_message_text = ADD_ITEM__INCORRECT_URL_TEXT
        # noinspection PyUnboundLocalVariable
        if error.message == item.url_incorrect_domain_error_text:
            new_bot_message_text = ADD_ITEM__INCORRECT_DOMAIN_TEMPLATE.format(
                url = user_message.text,
                site_name = site.name
            )
        if not recursive:
            bot.edit_message_text(
                new_bot_message_text,
                bot_message.chat.id,
                bot_message.id,
                reply_markup = get_inline_keyboard_markup(
                    get_inline_cancel_button_row(
                        ADD_ITEM_COMMAND,
                        # в extras передается id инстанса TrackingSite
                        extras = site.id
                    )
                )
            )
        # выйти из рекурсии можно введя валидную ссылку на вещь или нажав кнопку отмены
        bot.register_next_step_handler(
            bot_message,
            add_item_get_url_step,
            bot_message,
            site,
            item_type,
            recursive = True
        )
    finally:
        bot.delete_message(user_message.chat.id, user_message.id)


def get_button_texts_for_sizes(item, remove_size_callback_prefix):
    texts = {x: x for x in item.sizes_on_site}
    if item.sizes is not None:
        for size in item.sizes:
            del texts[size]
            texts.update({f"убрать {size}": f"{remove_size_callback_prefix}{size}"})
    return texts


# todo: write remove_item_command
# todo: write change_item_sizes_command
# todo: write add_default_item_type_sizes_command
# todo: write remove_default_item_type_sizes_command
@bot.callback_query_handler(func = is_numbered_callback_handler(ADD_ITEM_COMMAND, 2))
@logger.log_telegram_callback
@cancel_button_in_callback
def add_item_callback_handler_2(callback):
    """Выбор размеров вещи."""

    callback_data = get_callback_data(callback)
    callback_extras = get_callback_extras(callback)
    item = models.Item.objects.get(id = int(callback_extras))
    remove_size_callback_prefix = "remove-"

    if callback_data == FINISH_BUTTON_TEXT_EN:
        if len(item.sizes_to_order) == 1:
            command_finish_text = ADD_ITEM__SUCCESS_FINISH_ONE_SIZE_TEMPLATE.format(
                item_name = item.name,
                sizes_to_order = item.sizes_to_order[0]
            )
        elif len(item.sizes_to_order) > 1:
            command_finish_text = ADD_ITEM__SUCCESS_FINISH_MANE_SIZES_TEMPLATE.format(
                item_name = item.name,
                sizes_to_order = ", ".join(item.sizes_to_order)
            )
        else:
            command_finish_text = ADD_ITEM__SUCCESS_FINISH_NO_SIZES_TEMPLATE.format(item_name = item.name)

        bot.edit_message_text(command_finish_text, callback.message.chat.id, callback.message.id, )
    else:
        if callback_data.startswith(remove_size_callback_prefix):
            item.sizes.remove(callback_data.removeprefix(remove_size_callback_prefix))
            item.save()
            logger.log_inside_telegram_command(
                logging.DEBUG,
                callback,
                f"\"{callback_data}\" size was removed for {item.discount_hunter_site_link.site.name} site"
                f" and item with url - ({item.url})."
            )
        else:
            item.sizes.append(callback_data)
            item.save()
            logger.log_inside_telegram_command(
                logging.DEBUG,
                callback,
                f"\"{callback_data}\" size was added for {item.discount_hunter_site_link.site.name} site"
                f" and item with url - ({item.url})."
            )

        next_handler_number = get_callback_handler_number(callback)
        buttons_names = get_button_texts_for_sizes(item, remove_size_callback_prefix)
        rows = get_inline_button_rows(
            ADD_ITEM_COMMAND,
            buttons_names,
            handler_number = next_handler_number,
            extras = callback_extras
        )
        reply_markup = get_inline_keyboard_markup(
            *rows,
            get_inline_finish_button_row(ADD_ITEM_COMMAND, next_handler_number, callback_extras)
        )
        bot.edit_message_text(
            ADD_ITEM__CHOOSE_SIZES_TEXT,
            callback.message.chat.id,
            callback.message.id,
            reply_markup = reply_markup
        )


@bot.message_handler(commands = [HELP_COMMAND])
@logger.log_telegram_command(HELP_COMMAND)
def help_command(message):
    """Выводит информацию о боте."""

    bot.send_message(message.chat.id, BOT_DESCRIPTION)


@bot.message_handler(commands = [COMMAND_LIST_COMMAND])
@logger.log_telegram_command(COMMAND_LIST_COMMAND)
def command_list_command(message):
    """Выводит список доступных команд."""

    bot.send_message(message.chat.id, get_command_list_text())


@bot.message_handler(content_types = ["text"])
def unrecognized_messages(message):
    """Дает ответ, если сообщение пользователя не было распознано."""

    bot.send_message(message.chat.id, UNRECOGNIZED_MESSAGE_RESPONSE)
