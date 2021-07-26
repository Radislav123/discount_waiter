

class DiscountWaiterException(Exception):
    """Базовое исключение для всех исключений проекта."""

    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        super().__init__(*args, **kwargs)


class ServiceAppException(DiscountWaiterException):
    """Базовое исключение для всех исключений модуля service_app."""


class UnknownItemAttributeException(ServiceAppException):
    pass


class UnknownSiteNameException(ServiceAppException):
    pass
