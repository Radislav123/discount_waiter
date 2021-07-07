from service_app.exceptions import DiscountWaiterException


class ScraperAppException(DiscountWaiterException):
    """Базовое исключение для всех исключений модуля scrapers_app."""


class HtmlElementNotFoundException(ScraperAppException):
    """Поднимается, если не был найден хотя бы один элемент на странице."""

    def __init__(self, message, not_found_attr_names, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.not_found_attr_names = not_found_attr_names
