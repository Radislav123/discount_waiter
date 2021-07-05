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


class ClothesDefaultSizes(models.Model):
    """Таблица с размерами одежды по-умолчанию."""

    discount_hunter_site_link = models.ForeignKey(DiscountHunterSiteLink, on_delete = models.PROTECT)
    type = models.ForeignKey(ClothesType, on_delete = models.PROTECT)
    sizes = ArrayField(base_field = models.CharField(max_length = 20))


class Clothes(models.Model):
    """Таблица с отслеживаемой одеждой."""

    name = models.CharField(max_length = 200, null = True)
    discount_hunter_site_link = models.ForeignKey(DiscountHunterSiteLink, on_delete = models.PROTECT)
    type = models.ForeignKey(ClothesType, on_delete = models.PROTECT)
    # ссылка на страницу одежды на сайте
    url = models.URLField(max_length = 400)
    sizes = ArrayField(base_field = models.CharField(max_length = 20))
    sizes_on_site = ArrayField(base_field = models.CharField(max_length = 20), null = True)

    @property
    def sizes_to_order(self):
        sizes_to_order = []
        clothes_default_sizes = ClothesDefaultSizes.objects.filter(
            discount_hunter_site_link = self.discount_hunter_site_link,
            type = self.type
        )
        if self.sizes is not None:
            sizes_to_order = self.sizes
        elif clothes_default_sizes.exists():
            sizes_to_order = clothes_default_sizes.first().sizes
        return sizes_to_order
