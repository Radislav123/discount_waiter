from telegram_bot_app.telegram_bot.handlers.commands.common import *


def show_sites_to_choose(command, message, choose_site_text, have_no_sites_text):

    buttons_data = get_discount_hunter_tracked_sites_names(message.chat.id)
    rows = get_inline_button_rows_with_cancel(command, buttons_data)
    # в обратный вызов передается название сайта
    reply_markup = get_inline_keyboard_markup(*rows)

    if len(rows) > 1:
        bot.send_message(message.chat.id, choose_site_text, reply_markup = reply_markup)
    else:
        bot.send_message(message.chat.id, have_no_sites_text)


def show_types_to_choose(command, callback, next_handler_number, choose_item_type_text):

    # в extras передается id инстанса Site
    buttons_extras = models.Site.objects.get(name = get_callback_data(callback)).id
    # выбор типа вещей
    rows = get_inline_button_rows(
        command,
        models.ItemType.rus_to_en,
        buttons_in_row = 2,
        handler_number = next_handler_number,
        extras = buttons_extras
    )
    reply_markup = get_inline_keyboard_markup(
        *rows,
        *get_inline_button_rows(
            command,
            ALL_ITEM_TYPES_BUTTONS_DATA,
            handler_number = next_handler_number,
            extras = buttons_extras
        ),
        get_inline_cancel_button_row(
            command,
            handler_number = next_handler_number,
            extras = buttons_extras
        )
    )

    bot.edit_message_text(
        choose_item_type_text,
        callback.message.chat.id,
        callback.message.id,
        reply_markup = reply_markup,
        disable_web_page_preview = True
    )


def show_items_to_choose(
        command,
        callback,
        next_handler_number,
        all_item_types,
        no_items_text,
        one_item_text,
        many_items_text
):

    callback_data = get_callback_data(callback)
    discount_hunter = get_discount_hunter(callback.message.chat.id)
    site = models.Site.objects.get(id = get_callback_extras(callback))
    if all_item_types:
        tracked_items = get_discount_hunter_tracked_items(discount_hunter, site)
    else:
        item_type = models.ItemType.objects.get(name_en = callback_data)
        tracked_items = get_discount_hunter_tracked_items(discount_hunter, site, item_type)
    # в обратный вызов передается id вещи
    buttons_data = {item.name: item.id for item in tracked_items}
    # одна вещь на строку
    rows = get_inline_button_rows(command, buttons_data, buttons_in_row = 1, handler_number = next_handler_number)
    reply_markup = get_inline_keyboard_markup(*rows)

    if len(rows) == 0:
        message_text = no_items_text
    elif len(rows) == 1:
        message_text = one_item_text
    else:
        message_text = many_items_text

    bot.edit_message_text(
        message_text,
        callback.message.chat.id,
        callback.message.id,
        reply_markup = reply_markup
    )
