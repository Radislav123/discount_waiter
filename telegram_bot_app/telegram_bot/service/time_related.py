import threading
import time


def delayed_task(time_offset, function, *args, **kwargs):
    def function_with_delay():
        # time_offset в секундах
        time.sleep(time_offset)
        return function(*args, **kwargs)
    thread = threading.Thread(target = function_with_delay)
    thread.start()
