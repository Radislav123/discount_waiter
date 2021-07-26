# не импортировать, а передавать в функции, потому что иначе, при выполнении команд django, открывается браузер
# from service_app.service import browser
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from service_app.exceptions import UnknownSiteNameException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


def clear_basket(site_data, browser):
    # todo: сделать общую функцию выбора сайта для модуля order
    if site_data.name == site_data.SITES_NAMES.ZARA:
        zara(site_data, browser)
    else:
        raise UnknownSiteNameException(f"unknown site name - {site_data.name}")


def zara(site_data, browser):
    def not_empty():
        try:
            browser.refresh()
            if el := WebDriverWait(browser, 1).until(presence_of_element_located((By.XPATH, remove_item_button_xpath))):
                return el
        except TimeoutException:
            return False

    remove_item_button_xpath = '//button[@class = "shop-cart-item__action"]'
    browser.get(site_data.basket_url)

    while remove_item_button_element := not_empty():
        remove_item_button_element.click()
