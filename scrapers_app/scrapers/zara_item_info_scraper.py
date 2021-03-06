from service_app.logger import get_logger
from scrapers_app.constants import *
from lxml import html
import requests
import copy
import re


logger = get_logger(__name__)


# аттрибут == элемент
class ZaraItemInfoScraper:
    NAME = "name"
    SIZES_ON_SITE = "sizes_on_site"
    COLORS_ON_SITE = "colors_on_site"
    PRICE = "current_price"

    # информация, которая должна быть
    elements = {
        NAME: ['//*[@class = "product-detail-info__name"]'],
        SIZES_ON_SITE: ['//*[@class = "product-detail-size-info__main-label"]'],
        COLORS_ON_SITE: ['//*[@class = "product-detail-color-selector__color-area"]/span'],
        PRICE: ['//*[@class = "price__amount-current"]']
    }

    def __init__(self, item):
        self.item = item
        self.html_tree = self.get_page_html_tree()
        # найденная на странице информация
        self.found_elements = {}
        # xpath-ы, по которым была найдена информация
        self.found_elements_xpaths = {}

    @logger.log_scraper_method
    def find_elements_on_page(self, elements = None):
        if elements is None:
            elements = self.elements.keys()
        for element_name in elements:
            for element_xpath in self.elements[element_name]:
                found_elements = self.html_tree.xpath(element_xpath)
                if len(found_elements) != 0:
                    self.found_elements.update({element_name: found_elements})
                    self.found_elements_xpaths.update({element_name: element_xpath})

    @logger.log_scraper_method
    def init_item(self, elements = None):
        if elements is None:
            elements = [self.NAME, self.SIZES_ON_SITE, self.COLORS_ON_SITE, self.PRICE]
        if self.NAME in elements:
            self.item.name = self.get_name()
        if self.SIZES_ON_SITE in elements:
            self.item.sizes_on_site = self.get_sizes()
        if self.COLORS_ON_SITE in elements:
            self.item.colors_on_site = self.get_colors()
        if self.PRICE in elements:
            self.item.current_price = self.get_price()

    def get_page_html_tree(self):
        response = requests.get(self.item.url, headers = HEADERS)
        logger.debug(f"{response}: {self.item.url}")
        return html.fromstring(response.text)

    def get_name(self):
        return self.found_elements[self.NAME][0].text

    def get_sizes(self):
        return [x.text for x in self.found_elements[self.SIZES_ON_SITE]] if self.item.has_sizes else []

    def get_colors(self):
        return [x.text for x in self.found_elements[self.COLORS_ON_SITE]] if self.item.has_colors else []

    def get_price(self):
        return int("".join(re.findall(r"\d+", self.found_elements[self.PRICE][0].text)))

    @property
    def not_found_elements(self):
        needed_elements = copy.copy(list(self.elements.keys()))
        if not self.item.has_sizes:
            needed_elements.remove(self.SIZES_ON_SITE)
        if not self.item.has_colors:
            needed_elements.remove(self.COLORS_ON_SITE)
        return [x for x in needed_elements if x not in self.found_elements]

    @property
    def found_all_elements(self):
        return len(self.not_found_elements) == 0
