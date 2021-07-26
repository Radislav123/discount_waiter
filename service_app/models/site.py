from django.db import models


class Site(models.Model):
    """Отслеживаемые сайты"""

    name = models.CharField(max_length = 50)
    url = models.URLField()
