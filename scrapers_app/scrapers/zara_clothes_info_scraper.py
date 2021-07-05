from service_app.logger import get_logger
from scrapers_app.constants import *
from lxml import html
import requests


logger = get_logger(__name__)


class ZaraClothesInfoScraper:

    @classmethod
    def run(cls, clothes):
        html_tree = cls.get_page_html_tree(clothes.url)
        clothes.name = cls.get_clothes_name(html_tree)
        clothes.sizes_on_site = cls.get_clothes_sizes(html_tree)

    @staticmethod
    def get_page_html_tree(url):
        response = requests.get(url, headers = HEADERS)
        logger.debug(f"{response}: {url}")
        return html.fromstring(response.text)

    @staticmethod
    def get_clothes_name(html_tree):
        xpath = '//*[@class = "product-detail-info__name"]'
        return html_tree.xpath(xpath)[0].text

    @staticmethod
    def get_clothes_sizes(html_tree):
        xpath = '//*[@class = "product-size-info__main-label"]'
        sizes = html_tree.xpath(xpath)
        return [x.text for x in sizes]
