from service_app.logger import get_logger
from scrapers_app.constants import *
from lxml import html
import requests
import copy


logger = get_logger(__name__)
NAME = "name"
SIZES_ON_SITE = "sizes_on_site"


# аттрибут == элемент
class ZaraItemInfoScraper:
    # информация, которая должна быть
    elements = {
        NAME: '//*[@class = "product-detail-info__name"]',
        SIZES_ON_SITE: '//*[@class = "product-size-info__main-label"]'
    }

    def __init__(self, item):
        self.item = item
        self.html_tree = self.get_page_html_tree()
        # информация, которая присутствует на самом деле
        self.found_elements = {}

    def find_elements_on_page(self):
        for attr_name in self.elements:
            attr_found_elements = self.html_tree.xpath(self.elements[attr_name])
            if len(attr_found_elements) != 0:
                self.found_elements.update({attr_name: attr_found_elements})

    def run(self):
        """Записывает в вещь информацию, которая есть на странице."""

        for attr_name in self.found_elements:
            setattr(self.item, attr_name, getattr(self, f"get_item_{attr_name}")())

    def get_page_html_tree(self):
        response = requests.get(self.item.url, headers = HEADERS)
        logger.debug(f"{response}: {self.item.url}")
        return html.fromstring(response.text)

    def get_item_name(self):
        return self.found_elements[NAME][0].text

    def get_item_sizes_on_site(self):
        return [x.text for x in self.found_elements[SIZES_ON_SITE]]

    @property
    def not_found_elements(self):
        needed_elements = copy.copy(list(self.elements.keys()))
        if self.item.type.has_no_sizes:
            needed_elements.remove(SIZES_ON_SITE)
        return [x for x in self.elements if x in needed_elements]

    @property
    def found_all_elements(self):
        return len(self.not_found_elements) == 0
