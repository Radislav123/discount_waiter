# этот импорт хэндлеров нужен, чтобы они зарегистрировались
# noinspection PyUnresolvedReferences
from telegram_bot_app.telegram_bot import handlers
from telegram_bot_app.telegram_bot.service import *
from service_app.logger import get_logger


logger = get_logger(__name__)


# todo: прочитать про хранение и обработку личных данных
if __name__ == '__main__':
    set_bot_command_list()
    logger.info("bot command list was sent")

    try:
        logger.info("telegram bot was started")

        # уровень info в консоль не пишется, но видеть, что бот запустился, хочется и в консоли
        running_on_local_machine_text = "running on the local machine"
        logger.info(running_on_local_machine_text)
        print(running_on_local_machine_text)

        bot.polling(none_stop = True)
    finally:
        logger.info("telegram bot was stopped\n")
