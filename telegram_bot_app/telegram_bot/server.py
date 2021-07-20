# этот импорт хендлеров нужен, чтобы они зарегистрировались
# noinspection PyUnresolvedReferences
from telegram_bot_app.telegram_bot import handlers
from telegram_bot_app.telegram_bot.service import *
from service_app.service.time_related import *
from service_app.logger import get_logger
from service_app import models


logger = get_logger(__name__)


if __name__ == '__main__':
    set_bot_command_list()
    logger.info("bot command list was sent")
    timeloop.start()
    add_job(models.Item.check_and_order, CHECK_AND_ORDER_TIMEDELTA)

    try:
        logger.info("telegram bot was started")

        # уровень info в консоль не пишется, но видеть, что бот запустился, хочется и в консоли
        running_on_local_machine_text = "running on the local machine"
        logger.info(running_on_local_machine_text)
        print(running_on_local_machine_text)

        bot.polling(none_stop = True)
    finally:
        timeloop.stop()
        logger.info("telegram bot was stopped\n")
