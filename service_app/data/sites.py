from dataclasses import dataclass


@dataclass
class SiteData:
    @dataclass
    class SiteNames:
        ZARA: str = "Zara"

        @property
        def list(self):
            return list(self.__dict__.keys())

    name: str
    url: str
    log_in_url: str
    log_out_url: str
    basket_url: str
    login_field_xpath: str
    password_field_xpath: str
    log_in_button_xpath: str
    log_out_button_xpath: str
    add_to_basket_button_xpath: str

    instances = dict()
    SITES_NAMES = SiteNames()

    def __post_init__(self):
        self.__class__.instances.update({self.name: self})


ZARA_DATA = SiteData(
    name = "Zara",
    url = "https://www.zara.com/ru/",
    log_in_url = "https://www.zara.com/ru/ru/logon",
    log_out_url = "https://www.zara.com/ru/ru/user/menu",
    basket_url = "https://www.zara.com/ru/ru/shop/cart",
    login_field_xpath = '//*[@name = "logonId"]',
    password_field_xpath = '//*[@name = "password"]',
    log_in_button_xpath = '//button[contains(@class, "logon") and not(contains(@class, "alternate"))]',
    log_out_button_xpath = '//*[@class = "layout-user-sidebar-link__link layout-user-sidebar__logout-link"]',
    add_to_basket_button_xpath = '//*[@class = "button__lines-wrapper"]/*[contains(text(), "Добавить в корзину")]',
)
