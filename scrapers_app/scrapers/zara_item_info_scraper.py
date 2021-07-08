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
        NAME: ['//*[@class = "product-detail-info__name"]'],
        SIZES_ON_SITE: ['//*[@class = "product-detail-size-info__main-label"]']
    }

    def __init__(self, item):
        self.item = item
        self.html_tree = self.get_page_html_tree()
        # информация, которая присутствует на самом деле
        self.found_elements = {}

    def find_elements_on_page(self):
        for attr_name in self.elements:
            for element_xpath in self.elements[attr_name]:
                attr_found_elements = self.html_tree.xpath(element_xpath)
                if len(attr_found_elements) != 0:
                    self.found_elements.update({attr_name: attr_found_elements})

    def run(self):
        """Записывает в вещь информацию, которая есть на странице."""

        self.item.name = self.get_item_name()
        self.item.sizes_on_site = self.get_sizes()

    def get_page_html_tree(self):
        response = requests.get(self.item.url, headers = HEADERS)
        logger.debug(f"{response}: {self.item.url}")
        return html.fromstring(response.text)

    def get_item_name(self):
        return self.found_elements[NAME][0].text

    def get_sizes(self):
        return [x.text for x in self.found_elements[SIZES_ON_SITE]] if self.item.has_sizes else []

    @property
    def not_found_elements(self):
        needed_elements = copy.copy(list(self.elements.keys()))
        if not self.item.has_sizes:
            needed_elements.remove(SIZES_ON_SITE)
        return [x for x in needed_elements if x not in self.found_elements]

    @property
    def found_all_elements(self):
        not_found_elements = self.not_found_elements
        found_all_elements = len(not_found_elements) == 0
        if len(not_found_elements) == 1 and SIZES_ON_SITE not in self.found_elements and not self.item.has_sizes:
            found_all_elements = True
        return found_all_elements
