import threading
import time


def delayed_task(time_offset, function, *args, **kwargs):
    thread = threading.Thread(target = function, args = args, kwargs = kwargs)
    # time_offset в секундах
    time.sleep(time_offset)
    thread.start()
