from telegram_bot_app.telegram_bot.commands import *


CANCEL_BUTTON_TEXT_RUS = "Отмена"
CANCEL_BUTTON_TEXT_EN = "Cancel"
FINISH_BUTTON_TEXT_RUS = "Закончить"
FINISH_BUTTON_TEXT_EN = "Finish"
RETURN_BUTTON_TEXT_RUS = "Вернуться"
RETURN_BUTTON_TEXT_EN = "Return"
NEXT_BUTTON_TEXT_RUS = "Дальше"
NEXT_BUTTON_TEXT_EN = "Next"

HAVE_NO_SITES_DEFAULT_TEXT = f"На данный момент у Вас нет отслеживаемых сайтов.\n" \
                             f"Чтобы добавить, воспользуйтесь командой \"/{ADD_SITE_COMMAND}\"."
# нет точки в конце
CHOOSE_SITE_DEFAULT_TEXT = "Выберите сайт из предложенных ниже"
# нет точки в конце
CHOOSE_ITEM_TYPE_DEFAULT_TEXT = "Выберите тип вещи из предложенных ниже"

BOT_DESCRIPTION = f"Бот для отслеживания скидок.\n" \
                  f"Для просмотра списка команд введите '/' или '/{COMMAND_LIST_COMMAND}'."

UNRECOGNIZED_MESSAGE_RESPONSE = f"Я Вас не понял, воспользуйтесь списком команд.\n/{COMMAND_LIST_COMMAND}"

# приветствие бота
START__RESPONSE_TEXT = f"Для использования бота нужно заводить \"левые\" аккаунты на отслеживаемых сайтах," \
                       f" так как логины и пароли сохраняются как есть и никак не защищаются.\n" \
                       f"{BOT_DESCRIPTION}"

ADD_SITE__CHOOSE_SITE_TEXT = f"{CHOOSE_SITE_DEFAULT_TEXT}, который хотите добавить."
ADD_SITE__HAVE_NO_SITES_TO_ADD_TEXT = "Нет доступных сайтов для добавления."
ADD_SITE__INPUT_LOGIN_TEMPLATE = "Введите Ваш логин на выбранном сайте ({site})."
ADD_SITE__INPUT_PASSWORD_TEMPLATE = "Введите Ваш пароль на выбранном сайте ({site})."
ADD_SITE__SUCCESS_FINISH_TEXT = f"Сайт добавлен для отслеживания.\n" \
                                f"Чтобы добавить сайт, воспользуйтесь командой \"/{ADD_SITE_COMMAND}\".\n" \
                                f"Чтобы удалить сайт, воспользуйтесь командой \"/{REMOVE_SITE_COMMAND}\".\n" \
                                f"Чтобы посмотреть Ваши отслеживаемые сайты, " \
                                f"воспользуйтесь командой \"/{TRACKED_SITES_COMMAND}\".\n" \
                                f"Чтобы добавить вещь, воспользуйтесь командой \"/{ADD_ITEM_COMMAND}\"."

REMOVE_SITE__CHOOSE_SITE_TEXT = f"{CHOOSE_SITE_DEFAULT_TEXT}, который хотите убрать из отслеживаемых."
REMOVE_SITE__HAVE_NO_SITES_TEXT = HAVE_NO_SITES_DEFAULT_TEXT
REMOVE_SITE__SUCCESS_FINISH_TEMPLATE = "Сайт \"{site}\" больше не отслеживается."

TRACKED_SITES__SUCCESS_RESPONSE_TEXT = "Ваши отслеживаемые сайты:"
TRACKED_SITES__HAVE_NO_SITES_TEXT = HAVE_NO_SITES_DEFAULT_TEXT

SITE_CREDENTIALS__CHOOSE_SITE_TEXT = f"{CHOOSE_SITE_DEFAULT_TEXT}," \
                                     f" логин и пароль от аккаунта которого хотите посмотреть.\n" \
                                     f"(сообщение с логином и паролем будет удалено через минуту, после получения)"
SITE_CREDENTIALS__HAVE_NO_SITES_TEXT = HAVE_NO_SITES_DEFAULT_TEXT
# время в секундах, по прошествии которого сообщение с логином и паролем будет удалено
DELETE_SITE_CREDENTIALS_OFFSET = 60

ADD_ITEM__CHOOSE_SITE_TEXT = f"{CHOOSE_SITE_DEFAULT_TEXT}, на котором была найдена вещь."
ADD_ITEM__HAVE_NO_SITES_TEXT = HAVE_NO_SITES_DEFAULT_TEXT
ADD_ITEM__CHOOSE_ITEM_TYPE_TEXT = f"{CHOOSE_ITEM_TYPE_DEFAULT_TEXT}."
ADD_ITEM__INPUT_URL_TEXT = "Введите ссылку на вещь."
ADD_ITEM__HAS_ITEM_SIZES_TEXT = "Есть ли у выбранной Вами вещи размеры?"
ADD_ITEM__INCORRECT_URL_TEXT = "Введенная ссылка некорректна, введите корректную ссылку на вещь."
ADD_ITEM__INCORRECT_DOMAIN_TEMPLATE = "Введенная ссылка ({url}) не принадлежит выбранному Вами сайту ({site_name})." \
                                      "Ведите корректную ссылку на вещь."
ADD_ITEM__NOT_FOUND_INFORMATION_TEMPLATE = "Бот не нашел необходимой информации на странице вещи\n({url}).\n" \
                                           "Вы могли ввести ссылку с нужного сайта ({site_name})," \
                                           " но с вещью другого типа, или вообще без какой-либо вещи.\n" \
                                           "Ведите корректную ссылку на вещь."
# todo: добавить строку про команду change_item_sizes_command в ADD_ITEM__CHOOSE_SIZES_TEXT
ADD_ITEM__CHOOSE_SIZES_TEXT = f"Выберите размер (или размеры) из предложенных ниже (они взяты со страницы вещи).\n" \
                              f"При нажатии на кнопку \"{FINISH_BUTTON_TEXT_RUS}\"," \
                              f" размеры будут взяты из Ваших размеров по умолчанию, для данного типа вещи." \
                              f"Если у Вас не заданы размеры по умолчанию, вещь заказана не будет."
ADD_ITEM__ONE_SIZE_TEMPLATE = "Вещь ({item_name})" \
                              " с размером ({sizes_to_order}) добавлена для отслеживания."
ADD_ITEM__MANY_SIZES_TEMPLATE = "Вещь ({item_name})" \
                                " с размерами ({sizes_to_order}) добавлена для отслеживания."
ADD_ITEM__NO_SIZES_TEMPLATE = "Вещь ({item_name}) добавлена для отслеживания без размеров."

TRACKED_ITEMS__CHOOSE_SITE_TEXT = f"{CHOOSE_SITE_DEFAULT_TEXT}, вещи с которого хотите увидеть."
TRACKED_ITEMS__HAVE_NO_SITES_TEXT = HAVE_NO_SITES_DEFAULT_TEXT
TRACKED_ITEMS__CHOOSE_ITEM_TYPE = f"Выберите тип вещей из предложенных ниже, которые хотите увидеть."
TRACKED_ITEMS__ONE_ITEM_TEMPLATE = "Ваша единственная вещь типа {item_type_name}:"
TRACKED_ITEMS__MANY_ITEMS_TEMPLATE = "Ваши вещи типа {item_type_name}:"
TRACKED_ITEMS__NO_ITEMS_TEMPLATE = "У Вас нет ни одной вещи типа {item_type_name}."
TRACKED_ITEMS__ONE_ITEM_ALL_TYPES_TEXT = "Ваша единственная вещь:"
TRACKED_ITEMS__MANY_ITEMS_ALL_TYPES_TEXT = "Ваши вещи:"
TRACKED_ITEMS__NO_ITEMS_ALL_TYPES_TEXT = "У Вас нет ни одной вещи."

# первый аргумент - команда, которая связана с обратным вызовом
# второй аргумент - номер хендлера (или шага)
# третий аргумент - передаваемые данные
# четвертый аргумент - дополнительные параметры через запятую
CALLBACK_DATA_TEMPLATE = "{command}:{handler_number}:{data}:{extras}"
CALLBACK_DATA_CANCEL_BUTTON_TEMPLATE = "{command}:{handler_number}:" + CANCEL_BUTTON_TEXT_EN + ":{extras}"
CALLBACK_DATA_FINISH_BUTTON_TEMPLATE = "{command}:{handler_number}:" + FINISH_BUTTON_TEXT_EN + ":{extras}"
CALLBACK_DATA_RETURN_BUTTON_TEMPLATE = "{command}:{handler_number}:" + RETURN_BUTTON_TEXT_EN + ":{extras}"
CALLBACK_DATA_NEXT_BUTTON_TEMPLATE = "{command}:{handler_number}:" + NEXT_BUTTON_TEXT_EN + ":{extras}"
# третья группа содержит данные
CALLBACK_REGEX_TEMPLATE = r"(\b\w*\b)(:)(\d*)(:)(.*)(:)(.*)"
