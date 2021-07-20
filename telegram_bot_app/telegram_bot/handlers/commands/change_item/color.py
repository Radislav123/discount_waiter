from telegram_bot_app.telegram_bot.handlers.commands.common import *


logger = get_logger(__name__)


@bot.message_handler(commands = [CHANGE_ITEM_COLOR_COMMAND])
@logger.log_telegram_command(CHANGE_ITEM_COLOR_COMMAND)
def change_item_color_command(message):
    """Позволяет изменить заказываемый цвет вещи."""

    show_sites_to_choose(
        CHANGE_ITEM_COLOR_COMMAND,
        message,
        CHANGE_ITEM_COLOR__CHOOSE_SITE_TEXT,
        CHANGE_ITEM_COLOR__HAVE_NO_SITES_TEXT
    )


@bot.callback_query_handler(func = is_callback_handler(CHANGE_ITEM_COLOR_COMMAND, 0))
@logger.log_telegram_callback
@cancel_button_in_callback
def change_item_color_callback_handler(callback):
    """Получение сайта, заказываемый цвет вещи с которого будет изменен."""

    show_item_types_to_choose(CHANGE_ITEM_COLOR_COMMAND, callback, 1, CHANGE_ITEM_COLOR__CHOOSE_ITEM_TYPE_TEXT)


@bot.callback_query_handler(func = is_callback_handler(CHANGE_ITEM_COLOR_COMMAND, 1))
@logger.log_telegram_callback
@cancel_button_in_callback
def change_item_color_callback_handler_1(callback):
    """Получение типа вещи."""

    callback_data = get_callback_data(callback)
    all_item_types = callback_data == list(ALL_ITEM_TYPES_BUTTONS_DATA.values())[0]
    if all_item_types:
        texts = [
            CHANGE_ITEM_COLOR__NO_ITEMS_ALL_TYPES_TEXT,
            CHANGE_ITEM_COLOR__ONE_ITEM_ALL_TYPES_TEXT,
            CHANGE_ITEM_COLOR__MANY_ITEMS_ALL_TYPES_TEXT,
        ]
    else:
        item_type = models.ItemType.objects.get(name_en = callback_data)
        texts = [
            CHANGE_ITEM_COLOR__NO_ITEMS_TEMPLATE.format(item_type = item_type),
            CHANGE_ITEM_COLOR__ONE_ITEM_TEMPLATE.format(item_type = item_type),
            CHANGE_ITEM_COLOR__MANY_ITEMS_TEMPLATE.format(item_type = item_type)
        ]

    texts = list(map(escape_string, texts))
    show_items_to_choose(CHANGE_ITEM_COLOR_COMMAND, callback, 2, all_item_types, *texts)


@bot.callback_query_handler(func = is_callback_handler(CHANGE_ITEM_COLOR_COMMAND, 2))
@logger.log_telegram_callback
@cancel_button_in_callback
def change_item_color_callback_handler_2(callback):
    """Получение id вещи, заказываемый цвет которой, пользователь хочет изменить."""

    item = models.Item.objects.get(id = int(get_callback_data(callback)))
    next_handler_number = 3
    # в extras передается id инстанса Item
    buttons_extras = item.id
    rows = get_inline_button_rows_with_cancel(
        CHANGE_ITEM_COLOR_COMMAND,
        get_buttons_data_for_colors(item),
        handler_number = next_handler_number,
        extras = buttons_extras
    )
    reply_markup = get_inline_keyboard_markup(*rows)

    bot.edit_message_text(
        escape_string(CHANGE_ITEM_COLOR__CHOOSE_COLOR_TEMPLATE.format(url = item.url)),
        callback.message.chat.id,
        callback.message.id,
        parse_mode = MARKDOWN_PARSE_MODE,
        disable_web_page_preview = True,
        reply_markup = reply_markup
    )


# todo: добавить проверку item.has_colors
@bot.callback_query_handler(func = is_callback_handler(CHANGE_ITEM_COLOR_COMMAND, 3))
@logger.log_telegram_callback
@cancel_button_in_callback
def change_item_color_callback_handler_3(callback):
    """Выбор цвета вещи."""

    callback_data = get_callback_data(callback)
    callback_extras = get_callback_extras(callback)
    item = models.Item.objects.get(id = int(callback_extras))

    if callback_data.startswith(BUTTON_DATA_PREFIX_REMOVE):
        item.color = ""
        item.save()
        command_finish_text = escape_string(
            CHANGE_ITEM_COLOR__COLOR_UNSET_TEMPLATE.format(item_name = item.name, url = item.url)
        )
    else:
        item.color = callback_data
        item.save()
        command_finish_text = escape_string(
            CHANGE_ITEM_COLOR__COLOR_SET_TEMPLATE.format(item_name = item.name, url = item.url, color = callback_data)
        )

    bot.edit_message_text(
        command_finish_text,
        callback.message.chat.id,
        callback.message.id,
        parse_mode = MARKDOWN_PARSE_MODE,
        disable_web_page_preview = True
    )
