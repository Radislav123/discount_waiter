from selenium.webdriver.support.expected_conditions import visibility_of_any_elements_located
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from scrapers_app.order.common import timeout_to_no_such_element
from scrapers_app.exceptions import NotAllItemsInBasketException
from service_app.exceptions import UnknownSiteNameException
from selenium.webdriver.support.wait import WebDriverWait
from service_app.constants import LOAD_WAIT_TIMEOUT
from selenium.webdriver.common.by import By
import copy


def check_items_in_basket(ordered_items, site_data, browser):
    # todo: сделать общую функцию выбора сайта для модуля order
    if site_data.name == site_data.SITES_NAMES.ZARA:
        site_to_check = zara
    else:
        raise UnknownSiteNameException(f"unknown site name - {site_data.name}")

    browser.get(site_data.basket_url)
    not_checked_ordered_items = copy.copy(ordered_items)
    times_to_check = 3
    times_checked = 0
    items_ids_not_in_basket = []
    while times_checked < times_to_check:
        if times_checked > 0:
            browser.refresh()
        items_ids_not_in_basket = site_to_check(not_checked_ordered_items, browser)
        times_checked += 1
        if not items_ids_not_in_basket:
            # в корзине найдены все заказанные
            break
    else:
        if items_ids_not_in_basket:
            raise NotAllItemsInBasketException(f"items ids not in basket - {sorted(items_ids_not_in_basket)}")


def zara(not_checked_ordered_items, browser):
    def get_same_name_items_elements():
        # noinspection SpellCheckingInspection
        item_name_xpath = f'//*[@class = "shop-cart-item__description shop-cart-item__description--nolink"' \
                          f' and text() = "{item.name}"]/..'
        try:
            return wait.until(visibility_of_any_elements_located((By.XPATH, item_name_xpath)))
        except TimeoutException as error:
            raise timeout_to_no_such_element(error)

    def check_size():
        item_size_xpath = f'//*[contains(text(), "{size}")]'
        same_name_item_element.find_element_by_xpath(item_size_xpath)

    def check_color():
        item_color_xpath = f'//*[contains(text(), "{item.color}")]'
        if item.has_colors:
            same_name_item_element.find_element_by_xpath(item_color_xpath)

    items_ids_not_in_basket = []
    checked_ordered_items = []
    wait = WebDriverWait(browser, LOAD_WAIT_TIMEOUT)
    for item in not_checked_ordered_items:
        try:
            same_name_items_elements = get_same_name_items_elements()
            # название вещи проверять не нужно, потому что по нему искалась вещь в корзине
            for same_name_item_element in same_name_items_elements:
                if item.has_sizes:
                    for size in not_checked_ordered_items[item]:
                        check_size()
                        check_color()
                else:
                    check_color()
        except NoSuchElementException:
            items_ids_not_in_basket.append(item.id)
        else:
            checked_ordered_items.append(item)

    for item in checked_ordered_items:
        del not_checked_ordered_items[item]

    return items_ids_not_in_basket
