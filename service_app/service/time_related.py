from timeloop import Timeloop
import threading
import time


timeloop = Timeloop()


def delayed_task(time_offset, function, *args, **kwargs):
    def function_with_delay():
        # time_offset в секундах
        time.sleep(time_offset)
        return function(*args, **kwargs)
    thread = threading.Thread(target = function_with_delay)
    thread.start()


# type(interval) == timedelta (from datetime)
def add_job(function, interval, *args, **kwargs):
    # Use protected method because public does not have arguments for executable
    # noinspection PyProtectedMember
    timeloop._add_job(function, interval, *args, **kwargs)
