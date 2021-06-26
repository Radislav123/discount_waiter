from telegram_bot_app.telegram_bot.commands import *


BOT_DESCRIPTION = f"Бот для отслеживания скидок.\n" \
                  f"Для просмотра списка команд введите '/' или '/{COMMAND_LIST_COMMAND}'."

UNRECOGNIZED_MESSAGE_RESPONSE = f"Я Вас не понял, воспользуйтесь списком команд.\n/{COMMAND_LIST_COMMAND}"

START_COMMAND_RESPONSE_TEXT = f"Для использования бота нужно заводить \"левые\" аккаунты на отслеживаемых сайтах," \
                              f" так как логины и пароли сохраняются как есть и никак не защищаются.\n " \
                              f"{BOT_DESCRIPTION}"

ADD_SITE_COMMAND_RESPONSE_TEXT = "Выберите сайт, который хотите добавить, из предложенных ниже."
ADD_SITE_COMMAND_RESPONSE_TEXT_1 = "Нет доступных сайтов для добавления."
ADD_SITE_REQUEST_LOGIN_TEMPLATE = "Введите Ваш логин на выбранном сайте ({site_name})."
ADD_SITE_REQUEST_PASSWORD_TEMPLATE = "Введите Ваш пароль на выбранном сайте ({site_name})."
ADD_SITE_SUCCESS_RESPONSE_TEXT = f"Сайт добавлен для отслеживания.\n" \
                                 f"Чтобы добавить сайт, воспользуйтесь командой \"/{ADD_SITE_COMMAND}\".\n" \
                                 f"Чтобы удалить сайт, воспользуйтесь командой \"/{REMOVE_SITE_COMMAND}\".\n" \
                                 f"Чтобы посмотреть Ваши отслеживаемые сайты, " \
                                 f"воспользуйтесь командой \"/{TRACKED_SITES_COMMAND}\"."

REMOVE_SITE_COMMAND_RESPONSE_TEXT = "Выберите сайт, который хотите убрать из отслеживаемых, из предложенных ниже."
REMOVE_SITE_COMMAND_RESPONSE_TEXT_1 = f"На данный момент у Вас нет отслеживаемых сайтов.\n" \
                                      f"Чтобы добавить, воспользуйтесь командой \"/{ADD_SITE_COMMAND}\"."
REMOVE_SITE_SUCCESS_RESPONSE_TEMPLATE = "Сайт \"{site_name}\" больше не отслеживается."

GET_SITES_COMMAND_RESPONSE_TEXT = "Ваши отслеживаемые сайты:\n"
GET_SITES_COMMAND_RESPONSE_TEXT_1 = f"На данный момент у Вас нет отслеживаемых сайтов.\n" \
                                    f"Чтобы добавить, воспользуйтесь командой \"/{ADD_SITE_COMMAND}\"."

SITE_CREDENTIALS_RESPONSE_TEXT = "Выберите сайт, из предложенных ниже," \
                                 " логин и пароль от аккаунта которого хотите посмотреть.\n" \
                                 "(сообщение с логином и паролем будет удалено через минуту, после получения)"
SITE_CREDENTIALS_RESPONSE_TEXT_1 = f"На данный момент у Вас нет отслеживаемых сайтов.\n" \
                                   f"Чтобы добавить, воспользуйтесь командой \"/{ADD_SITE_COMMAND}\"."
# время в секундах, по прошествии которого сообщение с логином и паролем будет удалено
DELETE_SITE_CREDENTIALS_OFFSET = 60

ADD_CLOTHES_RESPONSE_TEXT = "Выберите тип одежды, из предложенных ниже."

CANCEL_BUTTON_TEXT = "Отмена"

# первый аргумент - команда, которая связана с обратным вызовом
# второй аргумент - передаваемые данные
CALLBACK_DATA_TEMPLATE = "{command} : {data}"
CALLBACK_DATA_CANCEL_TEMPLATE = "{command} : " + CANCEL_BUTTON_TEXT
# третья группа содержит данные
CALLBACK_REGEX_TEMPLATE = r"(\b\w*\b)( : )(.*)"
