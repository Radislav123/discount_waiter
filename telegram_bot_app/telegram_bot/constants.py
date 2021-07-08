from telegram_bot_app.telegram_bot.commands import *


MARKDOWN_PARSE_MODE = "MarkdownV2"

REMOVE_SIZE_PREFIX = "remove-"

CANCEL_BUTTON_TEXT_RUS = "Отмена"
CANCEL_BUTTON_TEXT_EN = "Cancel"
FINISH_BUTTON_TEXT_RUS = "Закончить"
FINISH_BUTTON_TEXT_EN = "Finish"
RETURN_BUTTON_TEXT_RUS = "Вернуться"
RETURN_BUTTON_TEXT_EN = "Return"
NEXT_BUTTON_TEXT_RUS = "Дальше"
NEXT_BUTTON_TEXT_EN = "Next"

HAVE_NO_SITES_DEFAULT_TEXT = f"На данный момент у Вас нет отслеживаемых сайтов.\n" \
                             f"Чтобы добавить, воспользуйтесь командой /{ADD_SITE_COMMAND}."
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
ADD_SITE__INPUT_LOGIN_TEMPLATE = "Введите Ваш логин на сайте [{site_name}]({site_url})"
ADD_SITE__INPUT_PASSWORD_TEMPLATE = "Введите Ваш пароль на сайте [{site_name}]({site_url})"
ADD_SITE__SUCCESS_FINISH_TEMPLATE = f"Сайт [{{site_name}}]({{site_url}}) добавлен для отслеживания.\n" \
                                    f"Чтобы убрать сайт из отслеживаемых," \
                                    f" воспользуйтесь командой /{REMOVE_SITE_COMMAND}.\n" \
                                    f"Чтобы посмотреть Ваши отслеживаемые сайты," \
                                    f" воспользуйтесь командой /{TRACKED_SITES_COMMAND}.\n" \
                                    f"Чтобы добавить вещь, воспользуйтесь командой /{ADD_ITEM_COMMAND}."

REMOVE_SITE__CHOOSE_SITE_TEXT = f"{CHOOSE_SITE_DEFAULT_TEXT}, который хотите убрать из отслеживаемых."
REMOVE_SITE__HAVE_NO_SITES_TEXT = HAVE_NO_SITES_DEFAULT_TEXT
REMOVE_SITE__SUCCESS_FINISH_TEMPLATE = "Сайт [{site_name}]({site_url}) больше не отслеживается."

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
ADD_ITEM__INPUT_URL_TEXT = f"Введите ссылку на вещь.\n" \
                           f"Вещи идентифицируются по ссылкам на них, но проверки на то, что у пользователя уже есть" \
                           f" вещь с введенной ссылкой, нет\n" \
                           f"Поэтому не добавляйте одну и ту же вещь несколько раз.\n" \
                           f"Размеры можно изменить - /{CHANGE_ITEM_SIZES_COMMAND}," \
                           f" а вещь можно убрать из отслеживаемых - /{REMOVE_ITEM_COMMAND}."
ADD_ITEM__HAS_ITEM_SIZES_TEXT = "Есть ли у выбранной Вами вещи размеры?"
ADD_ITEM__INCORRECT_URL_TEXT = "Введенная ссылка некорректна, введите корректную ссылку на вещь."
ADD_ITEM__INCORRECT_DOMAIN_TEMPLATE = "Введенная [ссылка]({url})" \
                                      " не принадлежит выбранному сайту [{site_name}]({site_url}).\n" \
                                      "Ведите корректную ссылку на вещь."
ADD_ITEM__NOT_FOUND_INFORMATION_TEMPLATE = "Бот не нашел необходимой информации на [странице вещи]({url}).\n" \
                                           "Вы могли ввести ссылку с [нужного сайта]({site_url})," \
                                           " но с вещью другого типа, или вообще без какой-либо вещи.\n" \
                                           "Ведите корректную ссылку на вещь."
ADD_ITEM__CHOOSE_SIZES_TEMPLATE = f"Выберите размер или размеры из предложенных ниже," \
                                  f" они взяты со [страницы вещи]({{url}}).\n" \
                                  f"Чтобы убрать вещь из отслеживаемых," \
                                  f" воспользуйтесь командой /{REMOVE_ITEM_COMMAND}\n." \
                                  f"Чтобы посмотреть Ваши отслеживаемые вещи," \
                                  f" воспользуйтесь командой /{TRACKED_ITEMS_COMMAND}.\n" \
                                  f"Чтобы изменить размеры отслеживаемой вещи" \
                                  f" воспользуйтесь командой /{CHANGE_ITEM_SIZES_COMMAND}"
ADD_ITEM__ONE_SIZE_TEMPLATE = "Вещь - [{item_name}]({url}) - добавлена для отслеживания" \
                              " с размером {sizes_to_order}."
ADD_ITEM__MANY_SIZES_TEMPLATE = "Вещь - [{item_name}]({url}) - добавлена для отслеживания" \
                                " с размерами: {sizes_to_order}."
ADD_ITEM__NO_SIZES_TEMPLATE = "Вещь - [{item_name}]({url}) - добавлена для отслеживания без размеров."

TRACKED_ITEMS__CHOOSE_SITE_TEXT = f"{CHOOSE_SITE_DEFAULT_TEXT}, вещи с которого хотите увидеть."
TRACKED_ITEMS__HAVE_NO_SITES_TEXT = HAVE_NO_SITES_DEFAULT_TEXT
TRACKED_ITEMS__CHOOSE_ITEM_TYPE_TEXT = "Выберите, вещи какого типа из предложенных ниже хотите увидеть."
TRACKED_ITEMS__ONE_ITEM_TEMPLATE = "Ваша единственная вещь типа {item_type_name}:"
TRACKED_ITEMS__MANY_ITEMS_TEMPLATE = "Ваши вещи типа {item_type_name}:"
TRACKED_ITEMS__NO_ITEMS_TEMPLATE = "У Вас нет ни одной вещи типа {item_type_name}."
TRACKED_ITEMS__ONE_ITEM_ALL_TYPES_TEXT = "Ваша единственная вещь:"
TRACKED_ITEMS__MANY_ITEMS_ALL_TYPES_TEXT = "Ваши вещи:"
TRACKED_ITEMS__NO_ITEMS_ALL_TYPES_TEXT = "У Вас нет ни одной вещи."

REMOVE_ITEM__CHOOSE_SITE_TEXT = f"{CHOOSE_SITE_DEFAULT_TEXT}, вещь с которого хотите убрать из отслеживаемых."
REMOVE_ITEM__HAVE_NO_SITES_TEXT = HAVE_NO_SITES_DEFAULT_TEXT
REMOVE_ITEM__CHOOSE_ITEM_TYPE_TEXT = "Выберите, вещь какого типа из предложенных ниже" \
                                     " Вы хотите убрать из отслеживаемых."
REMOVE_ITEM__ONE_ITEM_TEMPLATE = "Ваша единственная вещь типа {item_type_name}:"
REMOVE_ITEM__MANY_ITEMS_TEMPLATE = "Ваши вещи типа {item_type_name}:"
REMOVE_ITEM__NO_ITEMS_TEMPLATE = "У Вас нет ни одной вещи типа {item_type_name}."
REMOVE_ITEM__ONE_ITEM_ALL_TYPES_TEXT = "Ваша единственная вещь:"
REMOVE_ITEM__MANY_ITEMS_ALL_TYPES_TEXT = "Ваши вещи:"
REMOVE_ITEM__NO_ITEMS_ALL_TYPES_TEXT = "У Вас нет ни одной вещи."
REMOVE_ITEM__SUCCESS_FINISH_TEMPLATE = "Вещь - [{item_name}]({url}) - убрана из отслеживаемых."

CHANGE_ITEM_SIZES__CHOOSE_SITE_TEXT = f"{CHOOSE_SITE_DEFAULT_TEXT}," \
                                      f" заказываемые размеры вещи с которого хотите изменить."
CHANGE_ITEM_SIZES__HAVE_NO_SITES_TEXT = HAVE_NO_SITES_DEFAULT_TEXT
CHANGE_ITEM_SIZES__CHOOSE_ITEM_TYPE_TEXT = "Выберите, вещи какого типа из предложенных ниже" \
                                           " Вы хотите изменить заказываемые размеры."
CHANGE_ITEM_SIZES__ONE_ITEM_TEMPLATE = "Ваша единственная вещь типа {item_type_name}:"
CHANGE_ITEM_SIZES__MANY_ITEMS_TEMPLATE = "Ваши вещи типа {item_type_name}:"
CHANGE_ITEM_SIZES__NO_ITEMS_TEMPLATE = "У Вас нет ни одной вещи типа {item_type_name}."
CHANGE_ITEM_SIZES__ONE_ITEM_ALL_TYPES_TEXT = "Ваша единственная вещь:"
CHANGE_ITEM_SIZES__MANY_ITEMS_ALL_TYPES_TEXT = "Ваши вещи:"
CHANGE_ITEM_SIZES__NO_ITEMS_ALL_TYPES_TEXT = "У Вас нет ни одной вещи."
CHANGE_ITEM_SIZES__CHOOSE_SIZES_TEMPLATE = f"Выберите размер или размеры из предложенных ниже," \
                                           f" они взяты со [страницы вещи]({{url}})."
CHANGE_ITEM_SIZES__ONE_SIZE_TEMPLATE = "Вещь - [{item_name}]({url}) - добавлена для отслеживания" \
                                       " с размером {sizes_to_order}."
CHANGE_ITEM_SIZES__MANY_SIZES_TEMPLATE = "Вещь - [{item_name}]({url}) - добавлена для отслеживания" \
                                         " с размерами: {sizes_to_order}."
CHANGE_ITEM_SIZES__NO_SIZES_TEMPLATE = "Вещь - [{item_name}]({url}) - добавлена для отслеживания без размеров."

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
