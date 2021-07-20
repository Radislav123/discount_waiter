from scrapers_app.scrapers.zara_item_info_scraper import ZaraItemInfoScraper
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models


class DiscountHunter(models.Model):
    """Пользователи бота."""

    # https://limits.tginfo.me/ru-RU
    telegram_chat_id = models.IntegerField()
    telegram_user_id = models.IntegerField()
    telegram_username = models.CharField(max_length = 40, null = True)
    telegram_user_first_name = models.CharField(max_length = 100, null = True)
    telegram_user_last_name = models.CharField(max_length = 100, null = True)


class Site(models.Model):
    """Отслеживаемые сайты"""

    name = models.CharField(max_length = 50)
    address = models.URLField()


class DiscountHunterSiteLink(models.Model):
    """Таблица для связи пользователей с отслеживаемыми ими сайтами."""

    discount_hunter = models.ForeignKey(DiscountHunter, on_delete = models.PROTECT)
    site = models.ForeignKey(Site, on_delete = models.PROTECT)
    login = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 100)
    active = models.BooleanField()


class ItemType(models.Model):
    """Таблица с типами вещей."""

    name_choices_en = (
        "headdress",
        "shawl or scarf",
        "outerwear",
        "suit",
        "blazer",
        "shirt",
        "t-shirt",
        "corsetry",
        "underwear",
        "glove product",
        "pants",
        "jeans",
        "hosiery",
        "footwear",
        "undefined",
    )
    name_choices_rus = (
        "головной убор",
        "платочно-шарфовое изделие",
        "верхняя одежда",
        "костюм",
        "пиджак",
        "рубашка",
        "футболка",
        "корсетное изделие",
        "нательное бельё",
        "перчаточное изделие",
        "брюки",
        "джинсы",
        "чулочно-носочное изделие",
        "обувь",
        "неопределенный",
    )
    en_to_rus = dict(zip(name_choices_en, name_choices_rus))
    rus_to_en = dict(zip(name_choices_rus, name_choices_en))
    name_en = models.CharField(choices = ((x, x) for x in name_choices_en), max_length = 40)
    name_rus = models.CharField(choices = ((x, x) for x in name_choices_rus), max_length = 40)


class Item(models.Model):
    """Таблица с отслеживаемыми вещами."""

    discount_hunter = models.ForeignKey(DiscountHunter, on_delete = models.PROTECT)
    site = models.ForeignKey(Site, on_delete = models.PROTECT)
    type = models.ForeignKey(ItemType, on_delete = models.PROTECT)
    # ссылка на страницу вещи на сайте
    url = models.URLField(max_length = 400)
    name = models.CharField(max_length = 200)
    has_sizes = models.BooleanField()
    sizes = ArrayField(base_field = models.CharField(max_length = 20), blank = True)
    sizes_on_site = ArrayField(base_field = models.CharField(max_length = 20))
    has_colors = models.BooleanField()
    color = models.CharField(max_length = 20, blank = True)
    colors_on_site = ArrayField(base_field = models.CharField(max_length = 20))
    current_price = models.IntegerField()
    # вещь заказывается при стоимости ниже или равной полю order_price
    order_price = models.IntegerField(blank = True)

    @property
    def sizes_to_order(self):
        if self.has_sizes:
            sizes_to_order = self.sizes
        else:
            sizes_to_order = []
        return sizes_to_order

    @property
    def url_incorrect_domain_error_text(self):
        return f"{self.url} is not from {self.site.name} site."

    def validate_url(self):
        # проверка на то, что введен корректный url
        URLValidator()(self.url)

        # проверка на то, что введен url с выбранного сайта
        site_scheme, site_url_without_scheme = self.site.address.split(':')
        site_url_without_scheme = site_url_without_scheme[2:]
        site_domain = site_url_without_scheme.split('/')[0]
        if not self.url.startswith(f"{site_scheme}://{site_domain}/"):
            raise ValidationError(self.url_incorrect_domain_error_text)

    @property
    def order_price_is_not_number_error_text(self):
        return f"Order price ({self.order_price}) must be int or string representation of an int."

    def validate_order_price(self):
        # noinspection PyUnresolvedReferences
        if type(self.order_price) is str and not self.order_price.isdigit():
            raise ValidationError(self.order_price_is_not_number_error_text)

    @classmethod
    def check_and_order(cls, items = None):
        # todo: отвязать от Зары и выбирать из сайтов в базе
        elements_to_find = [ZaraItemInfoScraper.PRICE]
        if items is None:
            items = cls.objects.filter()
        for item in items:
            scraper = ZaraItemInfoScraper(item)
            scraper.find_elements_on_page(elements_to_find)
            scraper.init_item(elements_to_find)
            item.save()
            if item.current_price <= item.order_price:
                item.order()

    def order(self):
        # todo: сообщать пользователю, что вещь заказана
        pass
