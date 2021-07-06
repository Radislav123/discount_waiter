from service_app.logger import get_logger
from scrapers_app.constants import *
from lxml import html
import requests


logger = get_logger(__name__)


class ZaraItemInfoScraper:

    @classmethod
    def run(cls, item):
        html_tree = cls.get_page_html_tree(item.url)
        item.name = cls.get_item_name(html_tree)
        item.sizes_on_site = cls.get_item_sizes(html_tree)

    @staticmethod
    def get_page_html_tree(url):
        response = requests.get(url, headers = HEADERS)
        logger.debug(f"{response}: {url}")
        return html.fromstring(response.text)

    @staticmethod
    def get_item_name(html_tree):
        xpath = '//*[@class = "product-detail-info__name"]'
        return html_tree.xpath(xpath)[0].text

    @staticmethod
    def get_item_sizes(html_tree):
        xpath = '//*[@class = "product-size-info__main-label"]'
        sizes = html_tree.xpath(xpath)
        return [x.text for x in sizes]
