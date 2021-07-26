from service_app.constants import *
from service_app import models
from pathlib import Path
# noinspection PyPackageRequirements
import telebot
import logging


class ProjectFormatter(logging.Formatter):
    def format(self, record):
        if hasattr(record, REAL_FUNCTION_NAME):
            # noinspection PyUnresolvedReferences
            record.funcName = record.real_function_name
        if hasattr(record, REAL_FILENAME):
            # noinspection PyUnresolvedReferences
            record.filename = record.real_filename
        if hasattr(record, LOG_DECORATOR):
            # noinspection PyUnresolvedReferences
            if record.log_decorator:
                record.lineno = 0
        return super().format(record)


def get_function_real_filename(function):
    return function.__globals__["__file__"].split('\\')[-1]


def get_log_filepath(filename):
    return f"{LOG_FOLDER}/{filename}.log"


# хендлер для логов уровня "debug" и выше (в файл)
def get_debug_handler():
    log_filename = "debug"
    handler = logging.FileHandler(get_log_filepath(log_filename))
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(ProjectFormatter(LOG_FORMAT))
    return handler


# хендлер для логов уровня "info" и выше (в файл)
def get_info_handler():
    log_filename = "info"
    handler = logging.FileHandler(get_log_filepath(log_filename))
    handler.setLevel(logging.INFO)
    handler.setFormatter(ProjectFormatter(LOG_FORMAT))
    return handler


# хендлер для логов уровня "warning" и выше (в консоль)
def get_console_handler():
    handler = logging.StreamHandler()
    handler.setLevel(logging.WARNING)
    handler.setFormatter(ProjectFormatter(LOG_FORMAT))
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


# todo: rewrite logger to project class
# использовать только там, где прописана логика (как telegram_bot_app.telegram_bot.server)
def get_logger(logger_name):
    # создает папку для логов, если ее нет
    Path(LOG_FOLDER).mkdir(parents = True, exist_ok = True)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_debug_handler())
    logger.addHandler(get_info_handler())
    logger.addHandler(get_console_handler())

    def log_scraper_method(scraper_method):
        def wrapper(*args, **kwargs):
            log_extra = {
                REAL_FUNCTION_NAME: scraper_method.__name__,
                REAL_FILENAME: get_function_real_filename(scraper_method),
                LOG_DECORATOR: True
            }
            logger.debug(
                f"determines \"{scraper_method.__name__}\" scraper method call",
                extra = log_extra
            )
            result = scraper_method(*args, **kwargs)
            logger.debug(
                f"finishes \"{scraper_method.__name__}\" scraper method",
                extra = log_extra
            )
            return result

        return wrapper

    logger.log_scraper_method = log_scraper_method

    # для логирования начала и окончания выполнения команды Telegram-бота
    def log_telegram_command(command_name):
        def decorator(command_function):
            def wrapper(*args, **kwargs):
                telegram_message = args[0]
                user_identification = get_user_identification(telegram_message)
                log_extra = {
                    REAL_FUNCTION_NAME: command_function.__name__,
                    REAL_FILENAME: get_function_real_filename(command_function),
                    LOG_DECORATOR: True
                }
                logger.debug(
                    user_identification + f" - determines \"{command_name}\" command call",
                    extra = log_extra
                )
                result = command_function(*args, **kwargs)
                logger.debug(
                    user_identification + f" - finishes \"{command_name}\" command",
                    extra = log_extra
                )
                return result

            return wrapper

        return decorator

    logger.log_telegram_command = log_telegram_command

    # для логирования начала и окончания выполнения шага обратного вызова Telegram-бота
    def log_telegram_callback(callback_function):
        def wrapper(*args, **kwargs):
            callback = args[0]
            user_identification = get_user_identification(callback)
            log_extra = {
                REAL_FUNCTION_NAME: callback_function.__name__,
                REAL_FILENAME: get_function_real_filename(callback_function),
                LOG_DECORATOR: True
            }
            logger.debug(
                user_identification + f" - determines \"{callback_function.__name__}\" call",
                extra = log_extra
            )
            result = callback_function(*args, **kwargs)
            logger.debug(
                user_identification + f" - finishes \"{callback_function.__name__}\"",
                extra = log_extra
            )
            return result

        return wrapper

    logger.log_telegram_callback = log_telegram_callback

    # для логирования внутри команды (или обратного вызова) Telegram-бота
    def log_inside_telegram_command(log_level, telegram_message, log_message):
        log_message = get_user_identification(telegram_message) + " - " + log_message
        return logger.log(log_level, log_message)

    logger.log_inside_telegram_command = log_inside_telegram_command

    return logger
