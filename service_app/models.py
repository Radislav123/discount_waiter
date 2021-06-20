from django.contrib.postgres.fields import ArrayField
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


class ClothesType(models.Model):
    """Таблица с типами одежды."""

    name_choices = (
        ("underwear", "нательное бельё"),
        ("corsetry", "корсетное изделие"),
        ("outerwear", "верхняя одежда"),
        ("headdress", "головной убор"),
        ("hosiery", "чулочно-носочное изделие"),
        ("glove_product", "перчаточное изделие"),
        ("shawl_or_scarf", "платочно-шарфовое изделие"),
        ("footwear", "обувь"),
    )
    name = models.CharField(choices = name_choices, max_length = 40)


class ClothesDefaultSizes(models.Model):
    """Таблица с размерами одежды по-умолчанию."""

    discount_hunter_site_link = models.ForeignKey(DiscountHunterSiteLink, on_delete = models.PROTECT)
    type = models.ForeignKey(ClothesType, on_delete = models.PROTECT)
    sizes = ArrayField(base_field = models.CharField(max_length = 20))


class Clothes(models.Model):
    """Таблица с отслеживаемой одеждой."""

    discount_hunter_site_link = models.ForeignKey(DiscountHunterSiteLink, on_delete = models.PROTECT)
    type = models.ForeignKey(ClothesType, on_delete = models.PROTECT)
    # ссылка на страницу одежды на сайте
    link = models.URLField()
    # если min_size == max_size, то размер нужен только один
    min_size = models.CharField(max_length = 20)
    max_size = models.CharField(max_length = 20)