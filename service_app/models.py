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


class TrackingSite(models.Model):
    """Отслеживаемые сайты"""

    name = models.CharField(max_length = 50)
    address = models.URLField()


class DiscountHunterSiteLink(models.Model):
    """Таблица для связи пользователей с отслеживаемыми ими сайтами."""

    discount_hunter = models.ForeignKey(DiscountHunter, on_delete = models.PROTECT)
    site = models.ForeignKey(TrackingSite, on_delete = models.PROTECT)
    login = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 100)
    active = models.BooleanField()


class ItemType(models.Model):
    """Таблица с типами вещей."""

    name_choices_en = (
        "underwear",
        "corsetry",
        "outerwear",
        "headdress",
        "hosiery",
        "glove product",
        "shawl or scarf",
        "footwear",
        "undefined",
    )
    has_no_sizes_list = ("shawl or scarf",)
    name_choices_rus = (
        "нательное бельё",
        "корсетное изделие",
        "верхняя одежда",
        "головной убор",
        "чулочно-носочное изделие",
        "перчаточное изделие",
        "платочно-шарфовое изделие",
        "обувь",
        "неопределенный",
    )
    en_to_rus = dict(zip(name_choices_en, name_choices_rus))
    rus_to_en = dict(zip(name_choices_rus, name_choices_en))
    name = models.CharField(choices = ((x, x) for x in name_choices_en), max_length = 40)
    name_rus = models.CharField(choices = ((x, x) for x in name_choices_rus), max_length = 40)
    has_no_sizes = models.BooleanField()


class ItemDefaultSizes(models.Model):
    """Таблица с размерами вещей по-умолчанию."""

    discount_hunter_site_link = models.ForeignKey(DiscountHunterSiteLink, on_delete = models.PROTECT)
    type = models.ForeignKey(ItemType, on_delete = models.PROTECT)
    sizes = ArrayField(base_field = models.CharField(max_length = 20))


class Item(models.Model):
    """Таблица с отслеживаемыми вещами."""

    # поля, имеющие null = True заполняются информацией со страницы вещи
    name = models.CharField(max_length = 200, null = True)
    discount_hunter_site_link = models.ForeignKey(DiscountHunterSiteLink, on_delete = models.PROTECT)
    type = models.ForeignKey(ItemType, on_delete = models.PROTECT)
    # ссылка на страницу вещи на сайте
    url = models.URLField(max_length = 400)
    sizes = ArrayField(base_field = models.CharField(max_length = 20), blank = True)
    sizes_on_site = ArrayField(base_field = models.CharField(max_length = 20), null = True, blank = True)

    @property
    def sizes_to_order(self):
        sizes_to_order = []
        item_default_sizes = ItemDefaultSizes.objects.filter(
            discount_hunter_site_link = self.discount_hunter_site_link,
            type = self.type
        )
        if self.sizes is not None:
            sizes_to_order = self.sizes
        elif item_default_sizes.exists():
            sizes_to_order = item_default_sizes.first().sizes
        return sizes_to_order

    @property
    def url_incorrect_domain_error_text(self):
        return f"{self.url} is not from {self.discount_hunter_site_link.site.name} site."

    def validate_url(self):
        # проверка на то, что введен корректный url
        URLValidator()(self.url)
        # проверка на то, что введен url с выбранного сайта
        site_scheme, site_url_without_scheme = self.discount_hunter_site_link.site.address.split(':')
        site_url_without_scheme = site_url_without_scheme[2:]
        site_domain = site_url_without_scheme.split('/')[0]
        if not self.url.startswith(f"{site_scheme}://{site_domain}/"):
            raise ValidationError(self.url_incorrect_domain_error_text)
