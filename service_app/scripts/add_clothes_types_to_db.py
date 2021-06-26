from service_app.logger import get_logger
# noinspection PyUnresolvedReferences
import pep8_e402_import_django
from service_app import models


logger = get_logger(__name__)


def add_clothes_types():
    for type_name in zip(models.ClothesType.name_choices, models.ClothesType.name_choices_rus):
        clothes_type = models.ClothesType(
            name = type_name[0],
            name_rus = type_name[1]
        )
        if len(models.ClothesType.objects.filter(name = type_name[0])) == 0:
            clothes_type.save()
            logger.info(f"{type_name[0]} clothes type - successfully added to the db")
        else:
            update_data = clothes_type.__dict__.copy()
            del update_data["_state"]
            del update_data["id"]
            models.ClothesType.objects.filter(name = type_name[0]).update(**update_data)
            logger.info(f"{type_name[0]} ({type_name[1]}) clothes type - successfully updated in the db")


def run():
    add_clothes_types()