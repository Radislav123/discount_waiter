from selenium.common.exceptions import NoSuchElementException


def timeout_to_no_such_element(exception):
    new_exception = NoSuchElementException()
    new_exception.__dict__.update(exception.__dict__)
    return new_exception
