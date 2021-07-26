from datetime import timedelta


CHECK_AND_ORDER_TIMEDELTA = timedelta(minutes = 5)

# в секундах
LOAD_WAIT_TIMEOUT = 3

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36" \
             " (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"

DATABASE_NAME = "discount_waiter"

LOG_FORMAT = f"[%(asctime)s] - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
LOG_FOLDER = "logs"

REAL_FUNCTION_NAME = "real_function_name"
REAL_FILENAME = "real_filename"
LOG_DECORATOR = "log_decorator"
