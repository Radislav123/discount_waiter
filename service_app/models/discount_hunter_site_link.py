from service_app.models.discount_hunter import DiscountHunter
from service_app.logger import get_logger
from service_app.models.site import Site
from django.db import models


logger = get_logger(__name__)


class DiscountHunterSiteLink(models.Model):
    """Таблица для связи пользователей с отслеживаемыми ими сайтами."""

    discount_hunter = models.ForeignKey(DiscountHunter, on_delete = models.PROTECT)
    site = models.ForeignKey(Site, on_delete = models.PROTECT)
    login = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 100)
    active = models.BooleanField()
    shop_city = models.CharField(max_length = 50)
    shop_address = models.CharField(max_length = 100)
