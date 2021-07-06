from service_app.scripts.add_item_types_to_db import add_item_types
from service_app.scripts.add_sites_to_db import add_sites


def run():
    add_sites()
    add_item_types()
