from telegram_bot_app.telegram_bot.commands import *


CANCEL_BUTTON_TEXT_RUS = "Отмена"
CANCEL_BUTTON_TEXT_EN = "Cancel"
FINISH_BUTTON_TEXT_RUS = "Закончить"
FINISH_BUTTON_TEXT_EN = "Finish"
RETURN_BUTTON_TEXT_RUS = "Вернуться"
RETURN_BUTTON_TEXT_EN = "Return"
NEXT_BUTTON_TEXT_RUS = "Дальше"
NEXT_BUTTON_TEXT_EN = "Next"

BOT_DESCRIPTION = f"Бот для отслеживания скидок.\n" \
                  f"Для просмотра списка команд введите '/' или '/{COMMAND_LIST_COMMAND}'."

UNRECOGNIZED_MESSAGE_RESPONSE = f"Я Вас не понял, воспользуйтесь списком команд.\n/{COMMAND_LIST_COMMAND}"

START_COMMAND_RESPONSE_TEXT = f"Для использования бота нужно заводить \"левые\" аккаунты на отслеживаемых сайтах," \
                              f" так как логины и пароли сохраняются как есть и никак не защищаются.\n" \
                              f"{BOT_DESCRIPTION}"

ADD_SITE_COMMAND_RESPONSE_TEXT = "Выберите сайт, который хотите добавить, из предложенных ниже."
ADD_SITE_COMMAND_RESPONSE_TEXT_1 = "Нет доступных сайтов для добавления."
ADD_SITE_REQUEST_LOGIN_TEMPLATE = "Введите Ваш логин на выбранном сайте ({site_name})."
ADD_SITE_REQUEST_PASSWORD_TEMPLATE = "Введите Ваш пароль на выбранном сайте ({site_name})."
ADD_SITE_SUCCESS_RESPONSE_TEXT = f"Сайт добавлен для отслеживания.\n" \
                                 f"Чтобы добавить сайт, воспользуйтесь командой \"/{ADD_SITE_COMMAND}\".\n" \
                                 f"Чтобы удалить сайт, воспользуйтесь командой \"/{REMOVE_SITE_COMMAND}\".\n" \
                                 f"Чтобы посмотреть Ваши отслеживаемые сайты, " \
                                 f"воспользуйтесь командой \"/{TRACKED_SITES_COMMAND}\".\n" \
                                 f"Чтобы добавить вещь, воспользуйтесь командой \"/{ADD_ITEM_COMMAND}\"."

REMOVE_SITE_COMMAND_RESPONSE_TEXT = "Выберите сайт, который хотите убрать из отслеживаемых, из предложенных ниже."
REMOVE_SITE_COMMAND_RESPONSE_TEXT_1 = f"На данный момент у Вас нет отслеживаемых сайтов.\n" \
                                      f"Чтобы добавить, воспользуйтесь командой \"/{ADD_SITE_COMMAND}\"."
REMOVE_SITE_SUCCESS_RESPONSE_TEMPLATE = "Сайт \"{site_name}\" больше не отслеживается."

GET_SITES_COMMAND_RESPONSE_TEXT = "Ваши отслеживаемые сайты:\n"
GET_SITES_COMMAND_RESPONSE_TEXT_1 = f"На данный момент у Вас нет отслеживаемых сайтов.\n" \
                                    f"Чтобы добавить, воспользуйтесь командой \"/{ADD_SITE_COMMAND}\"."

SITE_CREDENTIALS_COMMAND_RESPONSE_TEXT = "Выберите сайт из предложенных ниже," \
                                         " логин и пароль от аккаунта которого хотите посмотреть.\n" \
                                         "(сообщение с логином и паролем будет удалено через минуту, после получения)"
SITE_CREDENTIALS_COMMAND_RESPONSE_TEXT_1 = f"На данный момент у Вас нет отслеживаемых сайтов.\n" \
                                           f"Чтобы добавить, воспользуйтесь командой \"/{ADD_SITE_COMMAND}\"."
# время в секундах, по прошествии которого сообщение с логином и паролем будет удалено
DELETE_SITE_CREDENTIALS_OFFSET = 60

ADD_ITEM_COMMAND_RESPONSE_TEXT = "Выберите сайт, на котором была найдена вещь из предложенных ниже."
ADD_ITEM_COMMAND_RESPONSE_TEXT_1 = f"На данный момент у Вас нет отслеживаемых сайтов.\n" \
                                   f"Чтобы добавить, воспользуйтесь командой \"/{ADD_SITE_COMMAND}\"."
ADD_ITEM_COMMAND_RESPONSE_TEXT_2 = "Выберите тип вещи из предложенных ниже."
ADD_ITEM_REQUEST_URL_TEXT = "Введите ссылку на вещь."
ADD_ITEM_INCORRECT_URL = "Введенная ссылка некорректна, введите корректную ссылку на вещь."
ADD_ITEM_INCORRECT_DOMAIN_TEMPLATE = "Введенная ссылка ({url}) не принадлежит выбранному вами сайту ({site_name})," \
                                     " введите корректную ссылку на вещь."
ADD_ITEM_NOT_FOUND_INFORMATION_TEXT = f"Бот не нашел необходимой информации на странице вещи.\n" \
                                      f"Вы могли ввести ссылку с нужного сайта, но с вещью другого типа," \
                                      f" или вообще без какой-либо вещи.\n" \
                                      f"Попробуйте вызвать команду еще раз ({ADD_ITEM_COMMAND})."
# todo: добавить строку про команду add_item_sizes_command в ADD_ITEM_REQUEST_SIZES_TEXT
ADD_ITEM_REQUEST_SIZES_TEXT = f"Выберите размер (или размеры) из предложенных ниже (они взяты со страницы вещи).\n" \
                              f"При нажатии на кнопку \"{FINISH_BUTTON_TEXT_RUS}\"," \
                              f" размеры будут взяты из Ваших размеров по умолчанию, для данного типа вещи." \
                              f"Если у Вас не заданы размеры по умолчанию, вещь заказана не будет."
ADD_ITEM_COMMAND_FINISH_TEMPLATE = "Вещь ({item_name})" \
                                   " с размером ({sizes_to_order}) добавлена для отслеживания."
ADD_ITEM_COMMAND_FINISH_TEMPLATE_1 = "Вещь ({item_name})" \
                                     " с размерами ({sizes_to_order}) добавлена для отслеживания."
# todo: добавить строку про использование команды add_item_default_sizes в ADD_ITEM_COMMAND_FINISH_TEMPLATE_1
ADD_ITEM_COMMAND_FINISH_TEMPLATE_2 = "Вещь ({item_name}) добавлена для отслеживания без размеров."

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
