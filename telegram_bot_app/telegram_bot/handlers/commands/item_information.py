from telegram_bot_app.telegram_bot.handlers.commands.common import *


logger = get_logger(__name__)


@bot.message_handler(commands = [ITEM_INFORMATION_COMMAND])
@logger.log_telegram_command(ITEM_INFORMATION_COMMAND)
def item_information_command(message):
    """Позволяет показать информацию о вещи."""

    show_sites_to_choose(
        ITEM_INFORMATION_COMMAND,
        message,
        ITEM_INFORMATION__CHOOSE_SITE_TEXT,
        ITEM_INFORMATION__HAVE_NO_SITES_TEXT
    )


@bot.callback_query_handler(func = is_callback_handler(ITEM_INFORMATION_COMMAND, 0))
@logger.log_telegram_callback
@cancel_button_in_callback
def item_information_callback_handler(callback):
    """Получение сайта, информация о вещи с которого будет показана."""

    show_item_types_to_choose(ITEM_INFORMATION_COMMAND, callback, 1, ITEM_INFORMATION__CHOOSE_ITEM_TYPE_TEXT)


@bot.callback_query_handler(func = is_callback_handler(ITEM_INFORMATION_COMMAND, 1))
@logger.log_telegram_callback
@cancel_button_in_callback
def item_information_callback_handler_1(callback):
    """Получение типа, информация вещи которого будет показана."""

    callback_data = get_callback_data(callback)
    all_item_types = callback_data == list(ALL_ITEM_TYPES_BUTTONS_DATA.values())[0]
    if all_item_types:
        texts = [
            ITEM_INFORMATION__NO_ITEMS_ALL_TYPES_TEXT,
            ITEM_INFORMATION__ONE_ITEM_ALL_TYPES_TEXT,
            ITEM_INFORMATION__MANY_ITEMS_ALL_TYPES_TEXT,
        ]
    else:
        item_type = models.ItemType.objects.get(name_en = callback_data)
        texts = [
            ITEM_INFORMATION__NO_ITEMS_TEMPLATE.format(item_type_name = item_type.name_rus),
            ITEM_INFORMATION__ONE_ITEM_TEMPLATE.format(item_type_name = item_type.name_rus),
            ITEM_INFORMATION__MANY_ITEMS_TEMPLATE.format(item_type_name = item_type.name_rus)
        ]

    texts = list(map(escape_string, texts))
    show_items_to_choose(ITEM_INFORMATION_COMMAND, callback, 2, all_item_types, *texts)


@bot.callback_query_handler(func = is_callback_handler(ITEM_INFORMATION_COMMAND, 2))
@logger.log_telegram_callback
@cancel_button_in_callback
def item_information_callback_handler_2(callback):
    """Получение id вещи, информацию о которой необходимо показать."""

    item = models.Item.objects.get(id = int(get_callback_data(callback)))
    item_information_text = ITEM_INFORMATION__ITEM_INFORMATION_COMMON_PART_TEMPLATE.format(
        item_name = item.name,
        item_url = item.url,
        order_price = item.order_price,
        current_price = item.current_price,
        site_name = item.site.name,
        site_url = item.site.url,
        item_type = item.type.name_rus
    )
    if item.has_sizes:
        item_information_text += '\n' + ITEM_INFORMATION__ITEM_INFORMATION_SIZES_PART_TEMPLATE.format(
            sizes = ", ".join(item.sizes),
            sizes_on_site = ", ".join(item.sizes_on_site)
        )
    if item.has_colors:
        item_information_text += '\n' + ITEM_INFORMATION__ITEM_INFORMATION_COLORS_PART_TEMPLATE.format(
            color = item.color,
            colors_on_site = ", ".join(item.colors_on_site)
        )
    item_information_text = escape_string(item_information_text)
    next_handler_number = 3

    bot.edit_message_text(
        item_information_text,
        callback.message.chat.id,
        callback.message.id,
        parse_mode = MARKDOWN_PARSE_MODE,
        disable_web_page_preview = True,
        reply_markup = get_inline_keyboard_markup(
            get_inline_finish_button_row(
                ITEM_INFORMATION_COMMAND,
                ITEM_INFORMATION__HIDE_ITEM_INFORMATION_BUTTON_TEXT,
                handler_number = next_handler_number
            )
        )
    )


@bot.callback_query_handler(func = is_callback_handler(ITEM_INFORMATION_COMMAND, 3))
@logger.log_telegram_callback
@cancel_button_in_callback
def item_information_callback_handler_3(callback):
    """Скрывает информацию о вещи."""

    if get_callback_data(callback) == FINISH_BUTTON_TEXT_EN:
        bot.edit_message_text(
            ITEM_INFORMATION__HIDE_ITEM_INFORMATION_TEXT,
            callback.message.chat.id,
            callback.message.id
        )
