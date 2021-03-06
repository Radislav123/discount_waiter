# noinspection PyUnresolvedReferences
import pep8_e402_import_django
from service_app.data.sites import SiteData
from service_app.logger import get_logger
from service_app import models


logger = get_logger(__name__)


def add_sites():
    for site_name in SiteData.instances:
        site_data = SiteData.instances[site_name]
        site = models.Site(
            name = site_data.name,
            url = site_data.url
        )

        if len(models.Site.objects.filter(name = site_data.name)) == 0:
            site.save()
            log_message = f"{site_data.name} site successfully added to the db"
        else:
            update_data = site.__dict__.copy()
            del update_data["_state"]
            del update_data["id"]
            models.Site.objects.filter(name = site_data.name).update(**update_data)
            log_message = f"{site_data.name} site successfully updated in the db"

        logger.info(log_message)
        print(log_message)


def run():
    add_sites()
