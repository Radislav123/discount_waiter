# не импортировать, а передавать в функции, потому что иначе, при выполнении команд django, открывается браузер
# from service_app.service import browser
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.action_chains import ActionChains
from service_app.exceptions import UnknownSiteNameException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from service_app.constants import LOAD_WAIT_TIMEOUT
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# если успешно заказана вещь без размеров, возвращается True
# если заказан успешно хотя бы один размер вещи с размерами, возвращается список заказанных размеров
def add_to_basket(site_data, scraper, browser):
    # todo: сделать общую функцию выбора сайта для модуля order
    if site_data.name == site_data.SITES_NAMES.ZARA:
        return zara(scraper, site_data, browser)
    else:
        raise UnknownSiteNameException(f"unknown site name - {site_data.name}")


def zara(scraper, site_data, browser):
    def choose_color():
        if scraper.item.has_colors:
            color_elements = browser.find_elements_by_xpath(
                scraper.found_elements_xpaths[scraper.COLORS_ON_SITE]
            )
            for color_element in color_elements:
                if color_element.get_attribute("textContent") == scraper.item.color:
                    color_element.find_element_by_xpath("..").click()

    def click_add_to_basket_button():
        element = WebDriverWait(browser, LOAD_WAIT_TIMEOUT) \
            .until(presence_of_element_located((By.XPATH, site_data.add_to_basket_button_xpath)))
        if not element.is_displayed():
            # кнопка добавления в корзину не помещается на экране
            # https://www.zara.com/ru/ru/%D0%BA%D0%BE%D0%B6%D0%B0%D0%BD%D1%8B%D0%B5-%D0%B1%D0%BE%D1%82%D0%B8%D0%BB%D1%8C%D0%BE%D0%BD%D1%8B-%D0%BD%D0%B0-%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B5-%D1%81-%D1%8D%D0%BB%D0%B0%D1%81%D1%82%D0%B8%D1%87%D0%BD%D1%8B%D0%BC%D0%B8-%D0%B2%D1%81%D1%82%D0%B0%D0%B2%D0%BA%D0%B0%D0%BC%D0%B8-%D0%BF%D0%BE-%D0%B1%D0%BE%D0%BA%D0%B0%D0%BC-p12135610.html?utm_campaign=productShare&utm_medium=mobile_sharing_iOS&utm_source=red_social_movil&v1=86344337
            ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform().click().send_keys(Keys.PAGE_UP).perform()
        else:
            element.click()
        # если кнопка не нажата по каким-либо причинам, будет поднято исключение
        return True

    browser.get(scraper.item.url)
    added_sizes = []
    if scraper.item.has_sizes:
        for size_number, size in enumerate(scraper.item.sizes, start = 1):
            size_in_stock_xpath = f'//*[@data-qa-action = "size-in-stock"]//*[contains(text(), "{size}")]'
            try:
                # todo: прокрутить, если размера не видно
                # https://www.zara.com/ru/ru/%D0%BA%D0%BE%D0%B6%D0%B0%D0%BD%D1%8B%D0%B5-%D1%88%D0%BB%D0%B5%D0%BF%D0%B0%D0%BD%D1%86%D1%8B-%D1%81-%D0%B4%D0%B2%D1%83%D0%BC%D1%8F-%D1%80%D0%B5%D0%BC%D0%B5%D1%88%D0%BA%D0%B0%D0%BC%D0%B8-p12703820.html?v1=125067909&v2=1886993
                size_element = WebDriverWait(browser, LOAD_WAIT_TIMEOUT) \
                    .until(presence_of_element_located((By.XPATH, size_in_stock_xpath)))
                size_element.click()
                choose_color()

                try:
                    click_add_to_basket_button()
                except TimeoutException:
                    continue

                added_sizes.append(size)
                if size_number < len(scraper.item.sizes):
                    browser.refresh()
            except TimeoutException:
                pass

        return added_sizes
    else:
        choose_color()
        try:
            return click_add_to_basket_button()
        except TimeoutException:
            pass
