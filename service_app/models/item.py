from service_app.models.discount_hunter import DiscountHunter
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from service_app.models.item_type import ItemType
from django.core.validators import URLValidator
from service_app.models.site import Site
from django.db import models


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
        site_scheme, site_url_without_scheme = self.site.url.split(':')
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
