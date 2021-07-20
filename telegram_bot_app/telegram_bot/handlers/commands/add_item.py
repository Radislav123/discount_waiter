from scrapers_app.scrapers.zara_item_info_scraper import ZaraItemInfoScraper
from telegram_bot_app.telegram_bot.handlers.commands.common import *
from django.core.exceptions import ValidationError
from distutils.util import strtobool
import logging


logger = get_logger(__name__)


@bot.message_handler(commands = [ADD_ITEM_COMMAND])
@logger.log_telegram_command(ADD_ITEM_COMMAND)
def add_item_command(message):
    """Позволяет добавить вещь для отслеживания."""

    # выбор сайта, на котором найдена вещь
    buttons_data = get_discount_hunter_tracked_sites_names(message.chat.id)
    rows = get_inline_button_rows_with_cancel(ADD_ITEM_COMMAND, buttons_data)
    # в обратный вызов передается название сайта
    reply_markup = get_inline_keyboard_markup(*rows)

    if len(rows) > 1:
        bot.send_message(message.chat.id, ADD_ITEM__CHOOSE_SITE_TEXT, reply_markup = reply_markup)
    else:
        bot.send_message(message.chat.id, ADD_ITEM__HAVE_NO_SITES_TEXT)


@bot.callback_query_handler(func = is_callback_handler(ADD_ITEM_COMMAND, 0))
@logger.log_telegram_callback
@cancel_button_in_callback
def add_item_callback_handler(callback):
    """Получение сайта, на котором была найдена вещь."""

    # в extras передается id инстанса Site
    buttons_extras = models.Site.objects.get(name = get_callback_data(callback)).id
    # выбор типа вещи
    next_handler_number = 1
    rows = get_inline_button_rows_with_cancel(
        ADD_ITEM_COMMAND,
        models.ItemType.rus_to_en,
        buttons_in_row = 2,
        handler_number = next_handler_number,
        extras = buttons_extras
    )
    reply_markup = get_inline_keyboard_markup(*rows)

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

    # в extras передается [id инстанса Site, id инстанса ItemType]
    buttons_extras = [
        get_callback_extras(callback),
        models.ItemType.objects.get(name_en = get_callback_data(callback)).id
    ]
    next_handler_number = 2
    rows = get_inline_button_rows_with_cancel(
        ADD_ITEM_COMMAND,
        TRUE_FALSE_BUTTONS_DATA,
        handler_number = next_handler_number,
        extras = buttons_extras
    )

    # спрашивается, есть ли у вещи размеры
    reply_markup = get_inline_keyboard_markup(*rows)

    bot.edit_message_text(
        ADD_ITEM__HAS_ITEM_SIZES_TEXT,
        callback.message.chat.id,
        callback.message.id,
        reply_markup = reply_markup
    )


@bot.callback_query_handler(func = is_callback_handler(ADD_ITEM_COMMAND, 2))
@logger.log_telegram_callback
@cancel_button_in_callback
def add_item_callback_handler_2(callback):
    """Получение ответа на вопрос - имеет ли вещь размеры."""

    # [id Site, id ItemType, bool имеет ли вещь размер]
    buttons_extras = [*get_callback_extras(callback), strtobool(get_callback_data(callback))]
    next_handler_number = 3
    rows = get_inline_button_rows_with_cancel(
        ADD_ITEM_COMMAND,
        TRUE_FALSE_BUTTONS_DATA,
        handler_number = next_handler_number,
        extras = buttons_extras
    )

    # спрашивается, есть ли у вещи цвет
    reply_markup = get_inline_keyboard_markup(*rows)

    bot.edit_message_text(
        ADD_ITEM__HAS_ITEM_COLORS_TEXT,
        callback.message.chat.id,
        callback.message.id,
        reply_markup = reply_markup
    )


@bot.callback_query_handler(func = is_callback_handler(ADD_ITEM_COMMAND, 3))
@logger.log_telegram_callback
@cancel_button_in_callback
def add_item_callback_handler_3(callback):
    """Получение ответа на вопрос - имеет ли вещь различные цвета."""

    site_id, item_type_id, has_colors = get_callback_extras(callback)
    # запрос на ввод ссылки на элемент одежды
    bot.edit_message_text(
        ADD_ITEM__INPUT_URL_TEXT,
        callback.message.chat.id,
        callback.message.id,
        reply_markup = get_inline_keyboard_markup(
            get_inline_cancel_button_row(ADD_ITEM_COMMAND, handler_number = 3)
        )
    )
    bot.register_next_step_handler(
        callback.message,
        add_item_get_url_step,
        callback.message,
        models.Site.objects.get(id = site_id),
        models.ItemType.objects.get(id = item_type_id),
        has_colors,
        strtobool(get_callback_data(callback))
    )


# todo: переделать хендлеры (сейчас взаимодействие с ботом в этой команде нелинейно и код запутан)
#  возможно, сделать похожими на эту функцию
def ask_sizes_color_order_price_or_finish(
        bot_message,
        item,
        sizes_asked = False,
        color_asked = False,
        order_price_asked = False
):
    # предполагается, что
    # номер хендлера для размеров == 4,
    # номер хендлера для цветов == sizes_handler_number + 1
    sizes_handler_number = 4

    # в extras передается id инстанса Item
    buttons_extras = item.id
    ask_order_price = False
    finish = False

    if item.has_sizes and not sizes_asked:
        # выбор размеров
        rows = get_inline_button_rows_with_finish(
            ADD_ITEM_COMMAND,
            item.sizes_on_site,
            handler_number = sizes_handler_number,
            extras = buttons_extras
        )
        reply_markup = get_inline_keyboard_markup(*rows)
        new_message_text = escape_string(ADD_ITEM__CHOOSE_SIZES_TEMPLATE.format(url = item.url))
    elif item.has_colors and not color_asked:
        # выбор цвета
        rows = get_inline_button_rows_with_finish(
            ADD_ITEM_COMMAND,
            item.colors_on_site,
            handler_number = sizes_handler_number + 1,
            extras = buttons_extras
        )
        reply_markup = get_inline_keyboard_markup(*rows)
        new_message_text = escape_string(ADD_ITEM__CHOOSE_COLOR_TEMPLATE.format(url = item.url))
    elif not order_price_asked:
        reply_markup = get_inline_keyboard_markup(
            get_inline_finish_button_row(ADD_ITEM_COMMAND, handler_number = 6, extras = item.id)
        )
        new_message_text = escape_string(ADD_ITEM__INPUT_ORDER_PRICE_TEMPLATE.format(url = item.url))
        ask_order_price = True
    else:
        reply_markup = get_inline_keyboard_markup(*[])
        new_message_text = get_command_finish_text(item)
        finish = True

    bot.edit_message_text(
        new_message_text,
        bot_message.chat.id,
        bot_message.id,
        parse_mode = MARKDOWN_PARSE_MODE,
        disable_web_page_preview = True,
        reply_markup = reply_markup
    )

    if ask_order_price:
        bot.register_next_step_handler(bot_message, add_item_get_order_price_step, bot_message, item)

    if finish:
        models.Item.check_and_order([item])


@logger.log_telegram_callback
def add_item_get_url_step(
        user_message,
        bot_message,
        site,
        item_type,
        has_sizes,
        has_colors,
        previous_error_message_text = None
):
    """Получение ссылки на вещь."""

    next_handler_number = 4
    try:
        # todo: добавить проверку на то, что такая вещь уже есть, если есть, предложить обновить ее данные
        item = models.Item(
            discount_hunter = get_discount_hunter(bot_message.chat.id),
            site = site,
            type = item_type,
            url = user_message.text,
            has_sizes = has_sizes,
            sizes = [],
            has_colors = has_colors,
            color = "",
            order_price = 0
        )
        item.validate_url()
        # поля name и sizes_on_site берутся с сайта
        # todo: отвязать от Зары и выбирать из сайтов в базе
        scraper = ZaraItemInfoScraper(item)
        scraper.find_elements_on_page()

        if scraper.found_all_elements:
            scraper.init_item()
            item.save()

            ask_sizes_color_order_price_or_finish(bot_message, item)
        else:
            new_bot_message_text = escape_string(
                ADD_ITEM__NOT_FOUND_INFORMATION_TEMPLATE.format(url = item.url, site_url = site.address)
            )
            if previous_error_message_text != new_bot_message_text:
                bot.edit_message_text(
                    new_bot_message_text,
                    bot_message.chat.id,
                    bot_message.id,
                    reply_markup = get_inline_keyboard_markup(
                        get_inline_cancel_button_row(
                            ADD_ITEM_COMMAND,
                            handler_number = next_handler_number,
                            # в extras передается id инстанса Site
                            extras = site.id
                        )
                    ),
                    parse_mode = MARKDOWN_PARSE_MODE,
                    disable_web_page_preview = True
                )
            log_message = f"not found elements ({scraper.not_found_elements})" \
                          f" on the page ({item.url})."
            logger.log_inside_telegram_command(
                logging.INFO,
                user_message,
                log_message
            )
            # выйти из рекурсии можно введя валидную ссылку на вещь или нажав кнопку отмены
            bot.register_next_step_handler(
                bot_message,
                add_item_get_url_step,
                bot_message,
                site,
                item_type,
                has_sizes,
                previous_error_message_text = new_bot_message_text
            )
    except ValidationError as error:
        new_bot_message_text = escape_string(ADD_ITEM__INCORRECT_URL_TEXT)
        # noinspection PyUnboundLocalVariable
        if error.message == item.url_incorrect_domain_error_text:
            new_bot_message_text = escape_string(
                ADD_ITEM__INCORRECT_DOMAIN_TEMPLATE.format(
                    url = user_message.text,
                    site_name = site.name,
                    site_url = site.address
                )
            )
        if previous_error_message_text != new_bot_message_text:
            bot.edit_message_text(
                new_bot_message_text,
                bot_message.chat.id,
                bot_message.id,
                parse_mode = MARKDOWN_PARSE_MODE,
                disable_web_page_preview = True,
                reply_markup = get_inline_keyboard_markup(
                    get_inline_cancel_button_row(
                        ADD_ITEM_COMMAND,
                        handler_number = next_handler_number,
                        # в extras передается id инстанса Site
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
            has_sizes,
            previous_error_message_text = new_bot_message_text
        )
    finally:
        bot.delete_message(user_message.chat.id, user_message.id)


def get_command_finish_text(item):
    if item.has_colors:
        command_finish_text = get_command_finish_text_with_color(item)
    else:
        command_finish_text = get_command_finish_text_without_color(item)
    return command_finish_text


def get_command_finish_text_without_color(item):
    if len(item.sizes_to_order) == 1:
        command_finish_text = escape_string(
            ADD_ITEM__ONE_SIZE_NO_COLOR_TEMPLATE.format(
                item_name = item.name,
                url = item.url,
                sizes_to_order = item.sizes_to_order[0],
                order_price = item.order_price
            )
        )
    elif len(item.sizes_to_order) > 1:
        command_finish_text = escape_string(
            ADD_ITEM__MANY_SIZES_NO_COLOR_TEMPLATE.format(
                item_name = item.name,
                url = item.url,
                sizes_to_order = ", ".join(item.sizes_to_order),
                order_price = item.order_price
            )
        )
    else:
        command_finish_text = escape_string(
            ADD_ITEM__NO_SIZES_NO_COLOR_TEMPLATE.format(
                item_name = item.name,
                url = item.url,
                order_price = item.order_price
            )
        )

    return command_finish_text


def get_command_finish_text_with_color(item):
    if len(item.sizes_to_order) == 1:
        command_finish_text = escape_string(
            ADD_ITEM__ONE_SIZE_WITH_COLOR_TEMPLATE.format(
                item_name = item.name,
                url = item.url,
                sizes_to_order = item.sizes_to_order[0],
                color = item.color,
                order_price = item.order_price
            )
        )
    elif len(item.sizes_to_order) > 1:
        command_finish_text = escape_string(
            ADD_ITEM__MANY_SIZES_WITH_COLOR_TEMPLATE.format(
                item_name = item.name,
                url = item.url,
                sizes_to_order = ", ".join(item.sizes_to_order),
                color = item.color,
                order_price = item.order_price
            )
        )
    else:
        command_finish_text = escape_string(
            ADD_ITEM__NO_SIZES_WITH_COLOR_TEMPLATE.format(
                item_name = item.name,
                url = item.url,
                color = item.color,
                order_price = item.order_price
            )
        )
    return command_finish_text


@bot.callback_query_handler(func = is_callback_handler(ADD_ITEM_COMMAND, 4))
@logger.log_telegram_callback
@cancel_button_in_callback
def add_item_callback_handler_4(callback):
    """Выбор размеров вещи."""

    callback_data = get_callback_data(callback)
    callback_extras = get_callback_extras(callback)
    item = models.Item.objects.get(id = int(callback_extras))
    next_handler_number = get_callback_handler_number(callback)

    if callback_data == FINISH_BUTTON_TEXT_EN:
        ask_sizes_color_order_price_or_finish(callback.message, item, True)
    else:
        if callback_data.startswith(BUTTON_DATA_PREFIX_REMOVE):
            item.sizes.remove(callback_data.removeprefix(BUTTON_DATA_PREFIX_REMOVE))
            item.save()
            logger.log_inside_telegram_command(
                logging.DEBUG,
                callback,
                f"\"{callback_data}\" size was removed for {item.site.name} site"
                f" and item with url - ({item.url})."
            )
        else:
            item.sizes.append(callback_data)
            item.sizes.sort()
            item.save()
            logger.log_inside_telegram_command(
                logging.DEBUG,
                callback,
                f"\"{callback_data}\" size was added for {item.site.name} site"
                f" and item with url - ({item.url})."
            )

        buttons_data = get_buttons_data_for_sizes(item)
        rows = get_inline_button_rows_with_finish(
            ADD_ITEM_COMMAND,
            buttons_data,
            handler_number = next_handler_number,
            extras = callback_extras
        )
        reply_markup = get_inline_keyboard_markup(*rows)

        bot.edit_message_text(
            escape_string(ADD_ITEM__CHOOSE_SIZES_TEMPLATE.format(url = item.url)),
            callback.message.chat.id,
            callback.message.id,
            parse_mode = MARKDOWN_PARSE_MODE,
            disable_web_page_preview = True,
            reply_markup = reply_markup
        )


@bot.callback_query_handler(func = is_callback_handler(ADD_ITEM_COMMAND, 5))
@logger.log_telegram_callback
def add_item_callback_handler_5(callback):
    """Выбор цвета вещи."""

    callback_data = get_callback_data(callback)
    callback_extras = get_callback_extras(callback)
    item = models.Item.objects.get(id = int(callback_extras))

    if callback_data != FINISH_BUTTON_TEXT_EN:
        item.color = callback_data
        item.save()

    ask_sizes_color_order_price_or_finish(callback.message, item, True, True)


@logger.log_telegram_callback
def add_item_get_order_price_step(user_message, bot_message, item):
    """Получение цены для заказа веши."""

    try:
        item.order_price = user_message.text
        item.validate_order_price()
        item.save()
        ask_sizes_color_order_price_or_finish(bot_message, item, True, True, True)
    except ValidationError:
        bot.edit_message_text(
            escape_string(
                ADD_ITEM__INCORRECT_ORDER_PRICE_TEMPLATE.format(order_price = item.order_price, url = item.url)
            ),
            bot_message.chat.id,
            bot_message.id,
            parse_mode = MARKDOWN_PARSE_MODE,
            disable_web_page_preview = True,
            reply_markup = get_inline_keyboard_markup(
                get_inline_finish_button_row(ADD_ITEM_COMMAND, handler_number = 6, extras = item.id)
            )
        )
        bot.register_next_step_handler(bot_message, add_item_get_order_price_step, bot_message, item)
    finally:
        bot.delete_message(user_message.chat.id, user_message.id)


@bot.callback_query_handler(func = is_callback_handler(ADD_ITEM_COMMAND, 6))
@logger.log_telegram_callback
def add_item_callback_handler_6(callback):
    """Завершение команды."""

    bot.clear_step_handler(callback.message)
    bot.edit_message_text(
        get_command_finish_text(models.Item.objects.get(id = get_callback_extras(callback))),
        callback.message.chat.id,
        callback.message.id,
        parse_mode = MARKDOWN_PARSE_MODE,
        disable_web_page_preview = True
    )
