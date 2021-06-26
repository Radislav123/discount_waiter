# noinspection PyUnresolvedReferences
import pep8_e402_import_django
from service_app.constants import TRACKING_SITES
from service_app.logger import get_logger
from service_app import models


logger = get_logger(__name__)


def add_sites():
    for site_name in TRACKING_SITES:
        site = models.TrackingSite(
            name = site_name,
            address = TRACKING_SITES[site_name]
        )
        if len(models.TrackingSite.objects.filter(name = site_name)) == 0:
            site.save()
            logger.info(f"{site_name} site - successfully added to the db")
        else:
            update_data = site.__dict__.copy()
            del update_data["_state"]
            del update_data["id"]
            models.TrackingSite.objects.filter(name = site_name).update(**update_data)
            logger.info(f"{site_name} site - successfully updated in the db")


def run():
    add_sites()
