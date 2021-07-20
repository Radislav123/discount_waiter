from telegram_bot_app.telegram_bot.handlers.commands.common import *


logger = get_logger(__name__)


@bot.message_handler(commands = [REMOVE_ITEM_COMMAND])
@logger.log_telegram_command(REMOVE_ITEM_COMMAND)
def remove_item_command(message):
    """Позволяет убрать вещь из отслеживаемых."""

    # выбор сайта, вещь с которого нужно убрать из отслеживаемых
    buttons_data = get_discount_hunter_tracked_sites_names(message.chat.id)
    rows = get_inline_button_rows(REMOVE_ITEM_COMMAND, buttons_data)
    # в обратный вызов передается название сайта
    reply_markup = get_inline_keyboard_markup(*rows, get_inline_cancel_button_row(REMOVE_ITEM_COMMAND))

    if len(rows) > 0:
        bot.send_message(message.chat.id, REMOVE_ITEM__CHOOSE_SITE_TEXT, reply_markup = reply_markup)
    else:
        bot.send_message(message.chat.id, REMOVE_ITEM__HAVE_NO_SITES_TEXT)


@bot.callback_query_handler(func = is_callback_handler(REMOVE_ITEM_COMMAND, 0))
@logger.log_telegram_callback
@cancel_button_in_callback
def remove_item_callback_handler(callback):
    """Получение сайта, вещи с которого будут показаны."""

    # в extras передается id инстанса Site
    buttons_extras = models.Site.objects.get(name = get_callback_data(callback)).id
    # выбор типа вещей
    next_handler_number = 1
    rows = get_inline_button_rows(
        REMOVE_ITEM_COMMAND,
        models.ItemType.rus_to_en,
        buttons_in_row = 2,
        handler_number = next_handler_number,
        extras = buttons_extras
    )
    reply_markup = get_inline_keyboard_markup(
        *rows,
        *get_inline_button_rows(
            REMOVE_ITEM_COMMAND,
            {"всех типов": "all"},
            handler_number = next_handler_number,
            extras = buttons_extras
        ),
        get_inline_cancel_button_row(
            REMOVE_ITEM_COMMAND,
            handler_number = next_handler_number,
            extras = buttons_extras
        )
    )

    bot.edit_message_text(
        REMOVE_ITEM__CHOOSE_ITEM_TYPE_TEXT,
        callback.message.chat.id,
        callback.message.id,
        reply_markup = reply_markup,
        disable_web_page_preview = True
    )


@bot.callback_query_handler(func = is_callback_handler(REMOVE_ITEM_COMMAND, 1))
@logger.log_telegram_callback
@cancel_button_in_callback
def remove_item_callback_handler_1(callback):
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
    rows = get_inline_button_rows(REMOVE_ITEM_COMMAND, buttons_data, buttons_in_row = 1, handler_number = 2)
    reply_markup = get_inline_keyboard_markup(*rows)

    if len(rows) > 0:
        if len(rows) == 1:
            if callback_data == "all":
                message_text = REMOVE_ITEM__ONE_ITEM_ALL_TYPES_TEXT
            else:
                # noinspection PyUnboundLocalVariable
                message_text = REMOVE_ITEM__ONE_ITEM_TEMPLATE.format(item_type_name = item_type.name_rus)
        else:
            if callback_data == "all":
                message_text = REMOVE_ITEM__MANY_ITEMS_ALL_TYPES_TEXT
            else:
                # noinspection PyUnboundLocalVariable
                message_text = REMOVE_ITEM__MANY_ITEMS_TEMPLATE.format(item_type_name = item_type.name_rus)
    else:
        if callback_data == "all":
            message_text = REMOVE_ITEM__NO_ITEMS_ALL_TYPES_TEXT
        else:
            # noinspection PyUnboundLocalVariable
            message_text = REMOVE_ITEM__NO_ITEMS_TEMPLATE.format(item_type_name = item_type.name_rus)
    bot.edit_message_text(
        message_text,
        callback.message.chat.id,
        callback.message.id,
        reply_markup = reply_markup
    )


@bot.callback_query_handler(func = is_callback_handler(REMOVE_ITEM_COMMAND, 2))
@logger.log_telegram_callback
@cancel_button_in_callback
def remove_item_callback_handler_2(callback):
    """Получение id вещи, которую пользователь хочет удалить."""

    item = models.Item.objects.get(id = int(get_callback_data(callback)))
    item.delete()
    bot.edit_message_text(
        escape_string(REMOVE_ITEM__SUCCESS_FINISH_TEMPLATE.format(item_name = item.name, item_url = item.url)),
        callback.message.chat.id,
        callback.message.id,
        parse_mode = MARKDOWN_PARSE_MODE,
        disable_web_page_preview = True
    )
