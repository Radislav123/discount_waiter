import scrapy


class ZaraSpider(scrapy.Spider):
    name = "ZaraSpider"

    def parse(self, response, **kwargs):
        """
        У каждого паука может быть несколько parse-функций.
        Присутствует, чтобы не было предупреждений у наследников,
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
            yield scrapy.Request(
                url = f"https://www.zara.com/ru/ru/search?searchTerm={article}",
                callback = self.parse_search_page
            )

    def parse_search_page(self, response: scrapy.http.Response):
        # '//select[@id = "criteria"]/option/text()'
        article_link_xpath = '//a[@class = "product-link product-grid-product__link link"]'
        # todo: remove print
        # p03427726.html?v1=85651229&v2=1718101
        # p03427414.html?v1=92162803
        print(f"------------\n\n{response.xpath(article_link_xpath).get()}\n\n------------")
        return {}
