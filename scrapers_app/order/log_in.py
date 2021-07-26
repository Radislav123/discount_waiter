from selenium.webdriver.support.expected_conditions import presence_of_element_located, url_changes
from scrapers_app.order.common import timeout_to_no_such_element
from service_app.exceptions import UnknownSiteNameException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from service_app.constants import LOAD_WAIT_TIMEOUT
from selenium.webdriver.common.by import By


def log_in(link, site_data, browser):
    # todo: сделать общую функцию выбора сайта для модуля order
    if site_data.name == site_data.SITES_NAMES.ZARA:
        zara(link, site_data, browser)
    else:
        raise UnknownSiteNameException(f"unknown site name - {site_data.name}")


def zara(link, site_data, browser):
    def check_log_in():
        user_menu_element_xpath = f'//*[@href = "{site_data.log_out_url}" and @aria-label = "Меню пользователя"]'
        try:
            wait.until(presence_of_element_located((By.XPATH, user_menu_element_xpath)))
        except TimeoutException as error:
            raise timeout_to_no_such_element(error)

    wait = WebDriverWait(browser, LOAD_WAIT_TIMEOUT)
    browser.get(site_data.log_in_url)
    wait.until(presence_of_element_located((By.XPATH, site_data.login_field_xpath))).send_keys(link.login)
    wait.until(presence_of_element_located((By.XPATH, site_data.password_field_xpath))).send_keys(link.password)
    browser.find_element_by_xpath(site_data.log_in_button_xpath).click()
    wait.until(url_changes(site_data.log_in_url))

    check_log_in()
