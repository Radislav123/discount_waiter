# Этот скрипт нужен, чтобы при использовании django в сторонних скриптах, как scrapy,
# не нарушалась рекомендация PEP8 E402 (https://pep8.readthedocs.io/en/release-1.7.x/intro.html)
# Импорт моделей django должен осуществляться строго после импорта этого скрипта

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'discount_waiter.settings')
import django       # noqa e402
django.setup()
