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


def is_callback_handler(command, handler_number = 0):
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

    tracking_sites_names = get_discount_hunter_tracked_sites_names(message.chat.id)
    buttons_data = [site.name for site in models.TrackedSite.objects.all()]
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
            site = tracking_site
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
    bot.edit_message_text(ADD_SITE__SUCCESS_FINISH_TEXT, bot_message.chat.id, bot_message.id)


# noinspection DuplicatedCode
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
def tracked_sites_command(message):
    """Выводит, отслеживаемые пользователем, сайты."""

    links = models.DiscountHunterSiteLink.objects.filter(
        discount_hunter = get_discount_hunter(message.chat.id),
        active = True
    )
    buttons_data = {link.site.name: link.site.address for link in links}
    rows = get_inline_button_rows(TRACKED_SITES_COMMAND, buttons_data, linked = True)

    if len(rows) > 0:
        reply_message = TRACKED_SITES__SUCCESS_RESPONSE_TEXT
    else:
        reply_message = TRACKED_SITES__HAVE_NO_SITES_TEXT
    reply_markup = get_inline_keyboard_markup(*rows)

    bot.send_message(message.chat.id, reply_message, reply_markup = reply_markup, disable_web_page_preview = True)


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


# noinspection DuplicatedCode
@bot.message_handler(commands = [ADD_ITEM_COMMAND])
@logger.log_telegram_command(ADD_ITEM_COMMAND)
def add_item_command(message):
    """Позволяет добавить вещь для отслеживания."""

    # выбор сайта, на котором найдена вещь
    buttons_data = get_discount_hunter_tracked_sites_names(message.chat.id)
    rows = get_inline_button_rows(ADD_ITEM_COMMAND, buttons_data)
    # в обратный вызов передается название сайта
    reply_markup = get_inline_keyboard_markup(*rows, get_inline_cancel_button_row(ADD_ITEM_COMMAND))

    if len(rows) > 0:
        bot.send_message(message.chat.id, ADD_ITEM__CHOOSE_SITE_TEXT, reply_markup = reply_markup)
    else:
        bot.send_message(message.chat.id, ADD_ITEM__HAVE_NO_SITES_TEXT)


# noinspection DuplicatedCode
@bot.callback_query_handler(func = is_callback_handler(ADD_ITEM_COMMAND, 0))
@logger.log_telegram_callback
@cancel_button_in_callback
def add_item_callback_handler(callback):
    """Получение сайта, на котором была найдена вещь."""

    # в extras передается id инстанса TrackedSite
    key_extras = models.TrackedSite.objects.get(name = get_callback_data(callback)).id
    # выбор типа вещи
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


@bot.callback_query_handler(func = is_callback_handler(ADD_ITEM_COMMAND, 1))
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
                # в extras передается id инстанса TrackedSite
                extras = get_callback_extras(callback)
            )
        )
    )
    bot.register_next_step_handler(
        callback.message,
        add_item_get_url_step,
        callback.message,
        models.TrackedSite.objects.get(id = get_callback_extras(callback)),
        models.ItemType.objects.get(name_en = get_callback_data(callback))
    )


# todo: сделать статистику экономии денег на скидках (и другую статистику)
@logger.log_telegram_callback
def add_item_get_url_step(user_message, bot_message, site, item_type, recursive = False):
    """Получение ссылки на вещь."""

    try:
        item = models.Item(
            discount_hunter_site_link = get_discount_hunter_site_link(
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
                        # в extras передается id инстанса TrackedSite
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
@bot.callback_query_handler(func = is_callback_handler(ADD_ITEM_COMMAND, 2))
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
            command_finish_text = ADD_ITEM__ONE_SIZE_TEMPLATE.format(
                item_name = item.name,
                sizes_to_order = item.sizes_to_order[0]
            )
        elif len(item.sizes_to_order) > 1:
            command_finish_text = ADD_ITEM__MANY_SIZES_TEMPLATE.format(
                item_name = item.name,
                sizes_to_order = ", ".join(item.sizes_to_order)
            )
        else:
            command_finish_text = ADD_ITEM__NO_SIZES_TEMPLATE.format(item_name = item.name)

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
        buttons_data = get_button_texts_for_sizes(item, remove_size_callback_prefix)
        rows = get_inline_button_rows(
            ADD_ITEM_COMMAND,
            buttons_data,
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


# todo: отвязать вещи от людей и идентифицировать их по ссылке на них (аналогично DiscountHunterSiteLink)
@bot.message_handler(commands = [TRACKED_ITEMS_COMMAND])
@logger.log_telegram_command(TRACKED_ITEMS_COMMAND)
def tracked_items_command(message):
    """Позволяет показать отслеживаемые вещи."""

    # выбор сайта, вещи на котором будут показаны
    buttons_data = get_discount_hunter_tracked_sites_names(message.chat.id)
    rows = get_inline_button_rows(TRACKED_ITEMS_COMMAND, buttons_data)
    reply_markup = get_inline_keyboard_markup(rows, get_inline_cancel_button_row(TRACKED_ITEMS_COMMAND))

    if len(rows) > 0:
        bot.send_message(message.chat.id, TRACKED_ITEMS__CHOOSE_SITE_TEXT, reply_markup = reply_markup)
    else:
        bot.send_message(message.chat.id, TRACKED_ITEMS__HAVE_NO_SITES_TEXT)


# noinspection DuplicatedCode
@bot.callback_query_handler(func = is_callback_handler(TRACKED_ITEMS_COMMAND, 0))
@logger.log_telegram_callback
@cancel_button_in_callback
def tracked_item_callback_handler(callback):
    """Получение сайта, вещи с которого будут показаны."""

    # в extras передается id инстанса TrackedSite
    key_extras = models.TrackedSite.objects.get(name = get_callback_data(callback)).id
    # выбор типа вещей
    next_handler_number = 1
    rows = get_inline_button_rows(
        TRACKED_ITEMS_COMMAND,
        models.ItemType.rus_to_en,
        buttons_in_row = 2,
        handler_number = next_handler_number,
        extras = key_extras
    )
    reply_markup = get_inline_keyboard_markup(
        *rows,
        get_inline_cancel_button_row(TRACKED_ITEMS_COMMAND, handler_number = next_handler_number, extras = key_extras)
    )

    bot.edit_message_text(
        TRACKED_ITEMS__CHOOSE_ITEM_TYPE,
        callback.message.chat.id,
        callback.message.id,
        reply_markup = reply_markup,
        disable_web_page_preview = True
    )


@bot.callback_query_handler(func = is_callback_handler(TRACKED_ITEMS_COMMAND, 1))
@logger.log_telegram_callback
@cancel_button_in_callback
def tracked_item_callback_handler_1(callback):
    """Получение типа вещей, которые будут показаны."""

    item_type = models.ItemType.objects.get(name_en = get_callback_data(callback))
    tracked_items = get_discount_hunter_tracked_items(
        callback.message.chat.id,
        models.TrackedSite.objects.get(id = int(get_callback_extras(callback))).name,
        item_type
    )
    buttons_data = {item.name: item.url for item in tracked_items}
    # одна вещь на строку
    rows = get_inline_button_rows(TRACKED_ITEMS_COMMAND, buttons_data, buttons_in_row = 1, linked = True)
    reply_markup = get_inline_keyboard_markup(*rows)

    if len(rows) > 0:
        if len(rows) == 1:
            message_text = TRACKED_ITEMS__ONE_ITEM_TEMPLATE.format(item_type.name_en)
        else:
            message_text = TRACKED_ITEMS__MANY_ITEMS_TEMPLATE.format(item_type.name_en)
        bot.edit_message_text(
            message_text,
            callback.message.chat.id,
            callback.message.id,
            reply_markup = reply_markup
        )
    else:
        bot.edit_message_text(
            TRACKED_ITEMS__NO_ITEMS_TEMPLATE.format(item_type.name_en),
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
