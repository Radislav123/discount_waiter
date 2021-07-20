from telegram_bot_app.telegram_bot.handlers.commands.common import *
from django.core.exceptions import ValidationError


logger = get_logger(__name__)


@bot.message_handler(commands = [CHANGE_ITEM_ORDER_PRICE_COMMAND])
@logger.log_telegram_command(CHANGE_ITEM_ORDER_PRICE_COMMAND)
def change_item_order_price_command(message):
    """Позволяет изменить заказываемую цену вещи."""

    show_sites_to_choose(
        CHANGE_ITEM_ORDER_PRICE_COMMAND,
        message,
        CHANGE_ITEM_ORDER_PRICE__CHOOSE_SITE_TEXT,
        CHANGE_ITEM_ORDER_PRICE__HAVE_NO_SITES_TEXT
    )


@bot.callback_query_handler(func = is_callback_handler(CHANGE_ITEM_ORDER_PRICE_COMMAND, 0))
@logger.log_telegram_callback
@cancel_button_in_callback
def change_item_order_price_callback_handler(callback):
    """Получение сайта, заказываемая цена вещи с которого будет изменена."""

    show_item_types_to_choose(
        CHANGE_ITEM_ORDER_PRICE_COMMAND,
        callback,
        1,
        CHANGE_ITEM_ORDER_PRICE__CHOOSE_ITEM_TYPE_TEXT
    )


@bot.callback_query_handler(func = is_callback_handler(CHANGE_ITEM_ORDER_PRICE_COMMAND, 1))
@logger.log_telegram_callback
@cancel_button_in_callback
def change_item_order_price_callback_handler_1(callback):
    """Получение типа вещи."""

    callback_data = get_callback_data(callback)
    all_item_types = callback_data == list(ALL_ITEM_TYPES_BUTTONS_DATA.values())[0]
    if all_item_types:
        texts = [
            CHANGE_ITEM_ORDER_PRICE__NO_ITEMS_ALL_TYPES_TEXT,
            CHANGE_ITEM_ORDER_PRICE__ONE_ITEM_ALL_TYPES_TEXT,
            CHANGE_ITEM_ORDER_PRICE__MANY_ITEMS_ALL_TYPES_TEXT,
        ]
    else:
        item_type = models.ItemType.objects.get(name_en = callback_data)
        texts = [
            CHANGE_ITEM_ORDER_PRICE__NO_ITEMS_TEMPLATE.format(item_type = item_type),
            CHANGE_ITEM_ORDER_PRICE__ONE_ITEM_TEMPLATE.format(item_type = item_type),
            CHANGE_ITEM_ORDER_PRICE__MANY_ITEMS_TEMPLATE.format(item_type = item_type)
        ]

    texts = list(map(escape_string, texts))
    show_items_to_choose(CHANGE_ITEM_ORDER_PRICE_COMMAND, callback, 2, all_item_types, *texts)


@bot.callback_query_handler(func = is_callback_handler(CHANGE_ITEM_ORDER_PRICE_COMMAND, 2))
@logger.log_telegram_callback
@cancel_button_in_callback
def change_item_order_price_callback_handler_2(callback):
    """Получение id вещи, заказываемую цену которой, пользователь хочет изменить."""

    item = models.Item.objects.get(id = int(get_callback_data(callback)))
    # в extras передается id инстанса Item
    buttons_extras = item.id
    reply_markup = get_inline_keyboard_markup(
        get_inline_cancel_button_row(
            CHANGE_ITEM_ORDER_PRICE_COMMAND,
            handler_number = get_callback_handler_number(callback),
            extras = buttons_extras
        )
    )

    bot.edit_message_text(
        escape_string(CHANGE_ITEM_ORDER_PRICE__INPUT_ORDER_PRICE_TEMPLATE.format(item_url = item.url)),
        callback.message.chat.id,
        callback.message.id,
        parse_mode = MARKDOWN_PARSE_MODE,
        disable_web_page_preview = True,
        reply_markup = reply_markup
    )
    bot.register_next_step_handler(
        callback.message,
        change_item_order_price_get_order_price_step,
        callback.message,
        item
    )


def change_item_order_price_get_order_price_step(user_message, bot_message, item):
    """Получение новой заказываемой цены вещи."""

    try:
        item.order_price = user_message.text
        item.validate_order_price()
        item.save()
        bot.edit_message_text(
            escape_string(
                CHANGE_ITEM_ORDER_PRICE__SUCCESS_FINISH_TEMPLATE.format(
                    item_name = item.name,
                    item_url = item.url,
                    order_price = item.order_price
                )
            ),
            bot_message.chat.id,
            bot_message.id,
            parse_mode = MARKDOWN_PARSE_MODE,
            disable_web_page_preview = True
        )
    except ValidationError:
        bot.edit_message_text(
            escape_string(
                CHANGE_ITEM_ORDER_PRICE__INCORRECT_ORDER_PRICE_TEMPLATE.format(
                    order_price = item.order_price,
                    item_url = item.url
                )
            ),
            bot_message.chat.id,
            bot_message.id,
            parse_mode = MARKDOWN_PARSE_MODE,
            disable_web_page_preview = True,
            reply_markup = get_inline_keyboard_markup(
                get_inline_cancel_button_row(CHANGE_ITEM_ORDER_PRICE_COMMAND, handler_number = 2, extras = item.id)
            )
        )
        bot.register_next_step_handler(bot_message, change_item_order_price_get_order_price_step, bot_message, item)
    finally:
        bot.delete_message(user_message.chat.id, user_message.id)
