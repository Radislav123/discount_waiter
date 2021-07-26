from selenium.webdriver.support.expected_conditions import presence_of_element_located, url_changes
from service_app.exceptions import UnknownSiteNameException
from selenium.webdriver.support.wait import WebDriverWait
from service_app.constants import LOAD_WAIT_TIMEOUT
from selenium.webdriver.common.by import By


def log_out(site_data, browser):
    # todo: сделать общую функцию выбора сайта для модуля order
    if site_data.name == site_data.SITES_NAMES.ZARA:
        zara(site_data, browser)
    else:
        raise UnknownSiteNameException(f"unknown site name - {site_data.name}")


def zara(site_data, browser):
    wait = WebDriverWait(browser, LOAD_WAIT_TIMEOUT)
    browser.get(site_data.log_out_url)
    wait.until(presence_of_element_located((By.XPATH, site_data.log_out_button_xpath))).click()
    wait.until(url_changes(site_data.log_out_url))
