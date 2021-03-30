import scrapy


class TestSpider(scrapy.Spider):
    """Базовый класс для всех пауков проекта."""

    name = "TestSpider"

    def parse(self, response, **kwargs):
        """
        У каждого паука может быть несколько parse-функций.
        Имплементирована, чтобы не было предупреждений у наследников,
        что не все абстрактные функции имплементированы.
        """
        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.articles = [
            "3427/414"
        ]

    def start_requests(self):
        """Задает список ссылок для начала скрапинга."""
        for article in self.articles:
            yield scrapy.Request(f"https://www.zara.com/ru/ru/search?searchTerm={article}", self.parse)

    def parse_search_page(self, response: scrapy.http.Response):
        # '//select[@id = "criteria"]/option/text()'
        article_link_xpath = '//a[@class = "product-link product-grid-product__link link"]'
        print(response.xpath(article_link_xpath).get())
