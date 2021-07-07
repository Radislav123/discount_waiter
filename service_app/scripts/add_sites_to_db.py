# noinspection PyUnresolvedReferences
import pep8_e402_import_django
from service_app.constants import TRACKED_SITES
from service_app.logger import get_logger
from service_app import models


logger = get_logger(__name__)


def add_sites():
    for site_name in TRACKED_SITES:
        site = models.TrackedSite(
            name = site_name,
            address = TRACKED_SITES[site_name]
        )

        if len(models.TrackedSite.objects.filter(name = site_name)) == 0:
            site.save()
            log_message = f"{site_name} site - successfully added to the db"
        else:
            update_data = site.__dict__.copy()
            del update_data["_state"]
            del update_data["id"]
            models.TrackedSite.objects.filter(name = site_name).update(**update_data)
            log_message = f"{site_name} site - successfully updated in the db"

        logger.info(log_message)
        print(log_message)


def run():
    add_sites()
