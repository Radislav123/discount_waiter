from django.contrib.postgres.fields import HStoreField
from django.db import models


# таблица с пользователями бота
class DiscountHunter(models.Model):
    # https://limits.tginfo.me/ru-RU
    telegram_username = models.CharField(max_length = 32)
    telegram_chat_id = models.IntegerField()
    clothes_links = models.URLField()
    # ключ           : значение
    # ClothesType.id : размер
    clothes_default_sizes = HStoreField()


class ClothesType(models.Model):
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


class Clothes(models.Model):
    type = models.ForeignKey(ClothesType, on_delete = models.PROTECT)
    # если min_size == max_size, то размер нужен только один,
    min_size = models.CharField(max_length = 20)
    max_size = models.CharField(max_length = 20)
