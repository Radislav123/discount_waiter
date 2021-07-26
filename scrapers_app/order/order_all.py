# не импортировать, а передавать в функции, потому что иначе, при выполнении команд django, открывается браузер
# from service_app.service import browser
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, url_contains, \
    presence_of_element_located
from selenium.webdriver.common.action_chains import ActionChains
from service_app.exceptions import UnknownSiteNameException
from selenium.webdriver.support.wait import WebDriverWait
from service_app.constants import LOAD_WAIT_TIMEOUT
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def order_all(link, site_data, browser):
    # todo: сделать общую функцию выбора сайта для модуля order
    if site_data.name == site_data.SITES_NAMES.ZARA:
        zara(link, site_data, browser)
    else:
        raise UnknownSiteNameException(f"unknown site name - {site_data.name}")


def zara(link, site_data, browser):
    def click_next_button():
        wait.until(presence_of_element_located((By.XPATH, next_button_xpath)))
        next_button = wait.until(element_to_be_clickable((By.XPATH, next_button_xpath)))
        next_button.click()

    wait = WebDriverWait(browser, LOAD_WAIT_TIMEOUT)
    next_button_xpath = '//*[@class = "button layout-shop-footer__body-button"]'
    browser.get(site_data.basket_url)
    if len(browser.find_elements_by_xpath(next_button_xpath)) == 0:
        browser.get(site_data.basket_url)
    click_next_button()

    # выбор способа доставки
    # на этапе выбора способа доставки, способ по умолчанию - в магазин
    wait.until(url_contains("/shipping/method-selection"))
    click_next_button()

    # выбор магазина для доставки
    choose_shop_path_part = "/shipping/physical-stores"
    choose_payment_method_path_part = "/payment/selection"
    wait.until(url_contains(choose_shop_path_part))
    address_form_xpath = '//*[@name = "search"]'
    input_address_text_field = wait.until(presence_of_element_located((By.XPATH, address_form_xpath)))
    input_address_text_field.clear()
    input_address_text_field.send_keys(link.shop_city)
    input_address_text_field.send_keys(Keys.RETURN)
    shop_name_xpath = f'//*[@class = "location-search-location__title" and contains(text(), "{link.shop_address}")]'
    wait.until(presence_of_element_located((By.XPATH, shop_name_xpath)))
    shop_address_element = wait.until(element_to_be_clickable((By.XPATH, shop_name_xpath)))
    # нужно кликнуть дважды (не опечатка)
    shop_address_element.click()
    shop_address_element.click()
    # click_next_button()
    browser.get(browser.current_url.replace(choose_shop_path_part, choose_payment_method_path_part))

    # выбор способа оплаты
    wait.until(url_contains(choose_payment_method_path_part))
    payment_method_element_xpath = '//*[@class = "payment-icon__name" and contains(text(), "Оплата при получении")]'
    payment_method_element = browser.find_element_by_xpath(payment_method_element_xpath).find_element_by_xpath("..")
    action_chain = ActionChains(browser)
    for i in range(4):
        action_chain.send_keys(Keys.ARROW_DOWN).perform()
    # нужно кликнуть дважды (не опечатка)
    payment_method_element.click()
    payment_method_element.click()
    click_next_button()

    # завершить заказ
    wait.until(url_contains("/order/summary"))
    terms_check_box_path = '//*[@type = "checkbox" and @name = "terms"]'
    wait.until(presence_of_element_located((By.XPATH, terms_check_box_path)))
    wait.until(element_to_be_clickable((By.XPATH, terms_check_box_path))).click()
    click_next_button()
