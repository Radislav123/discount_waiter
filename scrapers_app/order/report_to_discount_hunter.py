# не импортировать, а передавать в функции, потому что иначе, при выполнении команд django, открывается браузер
# from service_app.service import browser
from telegram_bot_app.telegram_bot.service import report_to_discount_hunter_in_telegram
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from service_app.exceptions import UnknownSiteNameException
from selenium.webdriver.support.wait import WebDriverWait
from service_app.constants import LOAD_WAIT_TIMEOUT
from selenium.webdriver.common.by import By


def report_to_discount_hunter(ordered_items, link, site_data, browser):
    # todo: сделать общую функцию выбора сайта для модуля order
    if site_data.name == site_data.SITES_NAMES.ZARA:
        zara(browser)
    else:
        raise UnknownSiteNameException(f"unknown site name - {site_data.name}")

    report_to_discount_hunter_in_telegram(ordered_items, link)


def zara(browser):
    success_order_text_xpath = '//*[contains(text(), "Заказ оформлен")]'
    WebDriverWait(browser, LOAD_WAIT_TIMEOUT) \
        .until(presence_of_element_located((By.XPATH, success_order_text_xpath)))
