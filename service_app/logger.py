from service_app.constants import LOG_FORMAT, LOG_FOLDER
from service_app import models
from pathlib import Path
# noinspection PyPackageRequirements
import telebot
import logging


def get_log_filepath(filename):
    return f"{LOG_FOLDER}/{filename}.log"


# хендлер для логов уровня "debug" и выше (в файл)
def get_debug_handler():
    log_filename = "debug"
    handler = logging.FileHandler(get_log_filepath(log_filename))
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return handler


# хендлер для логов уровня "info" и выше (в файл)
def get_normal_handler():
    log_filename = "normal"
    handler = logging.FileHandler(get_log_filepath(log_filename))
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return handler


# хендлер для логов уровня "warning" и выше (в консоль)
def get_console_handler():
    handler = logging.StreamHandler()
    handler.setLevel(logging.WARNING)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return handler


def get_user_identification(data):
    if type(data) is telebot.types.Message:
        user_identification = '{' + f"telegram_username: {data.from_user.username}, " \
                                    f"telegram_user_id: {data.from_user.id}, " \
                                    f"telegram_chat_id: {data.chat.id}" + "}"
    elif type(data) is telebot.types.CallbackQuery:
        user_identification = '{' + f"telegram_username: {data.from_user.username}, " \
                                    f"telegram_user_id: {data.from_user.id}, " \
                                    f"telegram_chat_id: {data.message.chat.id}" + "}"
    elif type(data) is models.DiscountHunter:
        user_identification = '{' + f"telegram_username: {data.telegram_username}, " \
                                    f"telegram_user_id: {data.telegram_user_id}, " \
                                    f"telegram_chat_id: {data.telegram_user_id}" + "}"
    else:
        user_identification = '{' + f"unknown user, data: {data}" + '}'
    return user_identification


# использовать только там, где прописана логика (как telegram_bot_app.telegram_bot.server)
def get_logger(logger_name):
    # создает папку для логов, если ее нет
    Path(LOG_FOLDER).mkdir(parents = True, exist_ok = True)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_debug_handler())
    logger.addHandler(get_normal_handler())
    logger.addHandler(get_console_handler())

    # для логирования начала и окончания выполнения команды Telegram-бота
    def log_telegram_command(command_name):
        def decorator(command_function):
            def wrapper(*args, **kwargs):
                telegram_message = args[0]
                user_identification = get_user_identification(telegram_message)
                logger.info(user_identification + f" - determines \"{command_name}\" command call")
                result = command_function(*args, **kwargs)
                logger.info(user_identification + f" - finishes \"{command_name}\" command")
                return result

            return wrapper

        return decorator

    logger.log_telegram_command = log_telegram_command

    # для логирования начала и окончания выполнения шага обратного вызова Telegram-бота
    def log_telegram_callback(callback_function):
        def wrapper(*args, **kwargs):
            callback = args[0]
            user_identification = get_user_identification(callback)
            logger.info(user_identification + f" - determines \"{callback_function.__name__}\" call")
            result = callback_function(*args, **kwargs)
            logger.info(user_identification + f" - finishes \"{callback_function.__name__}\"")
            return result

        return wrapper

    logger.log_telegram_callback = log_telegram_callback

    # для логирования внутри команды Telegram-бота
    def log_inside_telegram_command(log_level, telegram_message, log_message):
        log_message = get_user_identification(telegram_message) + " - " + log_message
        return logger.log(log_level, log_message)

    logger.log_inside_telegram_command = log_inside_telegram_command

    return logger
