from service_app.scripts.add_clothes_types_to_db import add_clothes_types
from service_app.scripts.add_sites_to_db import add_sites


def run():
    add_sites()
    add_clothes_types()
