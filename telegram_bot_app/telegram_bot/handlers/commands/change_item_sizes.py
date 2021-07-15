from telegram_bot_app.telegram_bot.handlers.commands.common import *


logger = get_logger(__name__)


@bot.message_handler(commands = [CHANGE_ITEM_SIZES_COMMAND])
@logger.log_telegram_command(CHANGE_ITEM_SIZES_COMMAND)
def change_item_sizes_command(message):
    """Позволяет изменить заказываемые размеры вещи."""

    # выбор сайта, вещь с которого нужно убрать из отслеживаемых
    buttons_data = get_discount_hunter_tracked_sites_names(message.chat.id)
    rows = get_inline_button_rows(CHANGE_ITEM_SIZES_COMMAND, buttons_data)
    # в обратный вызов передается название сайта
    reply_markup = get_inline_keyboard_markup(*rows, get_inline_cancel_button_row(CHANGE_ITEM_SIZES_COMMAND))

    if len(rows) > 0:
        bot.send_message(message.chat.id, CHANGE_ITEM_SIZES__CHOOSE_SITE_TEXT, reply_markup = reply_markup)
    else:
        bot.send_message(message.chat.id, CHANGE_ITEM_SIZES__HAVE_NO_SITES_TEXT)


@bot.callback_query_handler(func = is_callback_handler(CHANGE_ITEM_SIZES_COMMAND, 0))
@logger.log_telegram_callback
@cancel_button_in_callback
def change_item_sizes_callback_handler(callback):
    """Получение сайта, заказываемые размеры вещи с которого будут изменены."""

    # в extras передается id инстанса Site
    buttons_extras = models.Site.objects.get(name = get_callback_data(callback)).id
    # выбор типа вещей
    next_handler_number = 1
    rows = get_inline_button_rows(
        CHANGE_ITEM_SIZES_COMMAND,
        models.ItemType.rus_to_en,
        buttons_in_row = 2,
        handler_number = next_handler_number,
        extras = buttons_extras
    )
    reply_markup = get_inline_keyboard_markup(
        *rows,
        *get_inline_button_rows(
            CHANGE_ITEM_SIZES_COMMAND,
            ALL_ITEM_TYPES_BUTTONS_DATA,
            handler_number = next_handler_number,
            extras = buttons_extras
        ),
        get_inline_cancel_button_row(
            CHANGE_ITEM_SIZES_COMMAND,
            handler_number = next_handler_number,
            extras = buttons_extras
        )
    )

    bot.edit_message_text(
        CHANGE_ITEM_SIZES__CHOOSE_ITEM_TYPE_TEXT,
        callback.message.chat.id,
        callback.message.id,
        reply_markup = reply_markup,
        disable_web_page_preview = True
    )


@bot.callback_query_handler(func = is_callback_handler(CHANGE_ITEM_SIZES_COMMAND, 1))
@logger.log_telegram_callback
@cancel_button_in_callback
def change_item_sizes_callback_handler_1(callback):
    """Получение типа вещи."""

    callback_data = get_callback_data(callback)
    discount_hunter = get_discount_hunter(callback.message.chat.id)
    site = models.Site.objects.get(id = get_callback_extras(callback))
    if callback_data == "all":
        tracked_items = get_discount_hunter_tracked_items(discount_hunter, site)
    else:
        item_type = models.ItemType.objects.get(name_en = get_callback_data(callback))
        tracked_items = get_discount_hunter_tracked_items(discount_hunter, site, item_type)
    # в обратный вызов передается id вещи
    buttons_data = {item.name: item.id for item in tracked_items}
    # одна вещь на строку
    rows = get_inline_button_rows(CHANGE_ITEM_SIZES_COMMAND, buttons_data, buttons_in_row = 1, handler_number = 2)
    reply_markup = get_inline_keyboard_markup(*rows)

    if len(rows) > 0:
        if len(rows) == 1:
            if callback_data == "all":
                message_text = CHANGE_ITEM_SIZES__ONE_ITEM_ALL_TYPES_TEXT
            else:
                # noinspection PyUnboundLocalVariable
                message_text = CHANGE_ITEM_SIZES__ONE_ITEM_TEMPLATE.format(item_type_name = item_type.name_rus)
        else:
            if callback_data == "all":
                message_text = CHANGE_ITEM_SIZES__MANY_ITEMS_ALL_TYPES_TEXT
            else:
                # noinspection PyUnboundLocalVariable
                message_text = CHANGE_ITEM_SIZES__MANY_ITEMS_TEMPLATE.format(item_type_name = item_type.name_rus)
    else:
        if callback_data == "all":
            message_text = CHANGE_ITEM_SIZES__NO_ITEMS_ALL_TYPES_TEXT
        else:
            # noinspection PyUnboundLocalVariable
            message_text = CHANGE_ITEM_SIZES__NO_ITEMS_TEMPLATE.format(item_type_name = item_type.name_rus)
    bot.edit_message_text(
        message_text,
        callback.message.chat.id,
        callback.message.id,
        reply_markup = reply_markup
    )


@bot.callback_query_handler(func = is_callback_handler(CHANGE_ITEM_SIZES_COMMAND, 2))
@logger.log_telegram_callback
@cancel_button_in_callback
def change_item_sizes_callback_handler_2(callback):
    """Получение id вещи, заказываемые размеры которой, пользователь хочет изменить."""

    item = models.Item.objects.get(id = int(get_callback_data(callback)))
    next_handler_number = 3
    # в extras передается id инстанса Item
    buttons_extras = item.id
    rows = get_inline_button_rows(
        CHANGE_ITEM_SIZES_COMMAND,
        get_buttons_data_for_sizes(item),
        handler_number = next_handler_number,
        extras = buttons_extras
    )
    reply_markup = get_inline_keyboard_markup(
        *rows,
        get_inline_finish_button_row(
            CHANGE_ITEM_SIZES_COMMAND,
            handler_number = next_handler_number,
            extras = buttons_extras
        )
    )

    bot.edit_message_text(
        escape_string(CHANGE_ITEM_SIZES__CHOOSE_SIZES_TEMPLATE.format(url = item.url)),
        callback.message.chat.id,
        callback.message.id,
        parse_mode = MARKDOWN_PARSE_MODE,
        disable_web_page_preview = True,
        reply_markup = reply_markup
    )


# todo: добавить проверку item.has_sizes
@bot.callback_query_handler(func = is_callback_handler(CHANGE_ITEM_SIZES_COMMAND, 3))
@logger.log_telegram_callback
def change_item_sizes_callback_handler_3(callback):
    """Выбор размеров вещи."""

    callback_data = get_callback_data(callback)
    callback_extras = get_callback_extras(callback)
    item = models.Item.objects.get(id = int(callback_extras))

    if callback_data == FINISH_BUTTON_TEXT_EN:
        if len(item.sizes_to_order) == 1:
            command_finish_text = escape_string(
                CHANGE_ITEM_SIZES__ONE_SIZE_TEMPLATE.format(
                    item_name = item.name,
                    url = item.url,
                    sizes_to_order = item.sizes_to_order[0]
                )
            )
        elif len(item.sizes_to_order) > 1:
            command_finish_text = escape_string(
                CHANGE_ITEM_SIZES__MANY_SIZES_TEMPLATE.format(
                    item_name = item.name,
                    url = item.url,
                    sizes_to_order = ", ".join(item.sizes_to_order)
                )
            )
        else:
            command_finish_text = escape_string(
                CHANGE_ITEM_SIZES__NO_SIZES_TEMPLATE.format(item_name = item.name, url = item.url)
            )

        bot.edit_message_text(
            command_finish_text,
            callback.message.chat.id,
            callback.message.id,
            parse_mode = MARKDOWN_PARSE_MODE,
            disable_web_page_preview = True
        )
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

        next_handler_number = get_callback_handler_number(callback)
        buttons_data = get_buttons_data_for_sizes(item)
        rows = get_inline_button_rows(
            CHANGE_ITEM_SIZES_COMMAND,
            buttons_data,
            handler_number = next_handler_number,
            extras = callback_extras
        )
        reply_markup = get_inline_keyboard_markup(
            *rows,
            get_inline_finish_button_row(
                CHANGE_ITEM_SIZES_COMMAND,
                handler_number = next_handler_number,
                extras = callback_extras
            )
        )

        bot.edit_message_text(
            escape_string(CHANGE_ITEM_SIZES__CHOOSE_SIZES_TEMPLATE.format(url = item.url)),
            callback.message.chat.id,
            callback.message.id,
            parse_mode = MARKDOWN_PARSE_MODE,
            disable_web_page_preview = True,
            reply_markup = reply_markup
        )
