from django.db import models


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
