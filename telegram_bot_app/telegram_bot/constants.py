from telegram_bot_app.telegram_bot.commands import COMMAND_LIST_COMMAND


BOT_DESCRIPTION = f"Бот для отслеживания скидок.\n" \
                  f"Для просмотра списка команд введите '/' или '/{COMMAND_LIST_COMMAND}'."

UNRECOGNIZED_MESSAGE_RESPONSE = f"Я Вас не понял, воспользуйтесь списком команд.\n/{COMMAND_LIST_COMMAND}"

BOT_START_COMMAND_RESPONSE_TEXT = "Для использования бота нужно заводить \"левые\" аккаунты на отслеживаемых сайтах," \
                             " так как логины и пароли сохраняются как есть и никак не защищаются."
