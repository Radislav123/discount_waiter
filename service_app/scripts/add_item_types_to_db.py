from service_app.logger import get_logger
# noinspection PyUnresolvedReferences
import pep8_e402_import_django
from service_app import models


logger = get_logger(__name__)


def add_item_types():
    for name_en, name_rus in zip(models.ItemType.name_choices_en, models.ItemType.name_choices_rus):
        clothes_type = models.ItemType(name_en = name_en, name_rus = name_rus)

        if len(models.ItemType.objects.filter(name_en = name_en)) == 0:
            clothes_type.save()
            log_message = f"{name_en} clothes type - successfully added to the db"
        else:
            update_data = clothes_type.__dict__.copy()
            del update_data["_state"]
            del update_data["id"]
            models.ItemType.objects.filter(name_en = name_en).update(**update_data)
            log_message = f"{name_en} ({name_rus}) clothes type - successfully updated in the db"

        logger.info(log_message)
        print(log_message)


def run():
    add_item_types()
