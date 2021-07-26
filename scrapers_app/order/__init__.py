# не импортировать, а передавать в функции, потому что иначе, при выполнении команд django, открывается браузер
# from service_app.service import browser
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from scrapers_app.order.report_to_discount_hunter import report_to_discount_hunter
from scrapers_app.scrapers.zara_item_info_scraper import ZaraItemInfoScraper
from scrapers_app.order.check_items_in_basket import check_items_in_basket
from service_app.logger import get_logger, get_user_identification
from scrapers_app.exceptions import NotAllItemsInBasketException
from service_app.models import Item, DiscountHunterSiteLink
from scrapers_app.order.add_to_basket import add_to_basket
from scrapers_app.order.clear_basket import clear_basket
from scrapers_app.order.order_all import order_all
from scrapers_app.order.log_out import log_out
from scrapers_app.order.log_in import log_in
from service_app.data.sites import SiteData


logger = get_logger(__name__)
project_exceptions_to_restart = (NotAllItemsInBasketException,)
selenium_exceptions_to_restart = (StaleElementReferenceException, TimeoutException, NoSuchElementException)
exceptions_to_restart = tuple(project_exceptions_to_restart + selenium_exceptions_to_restart)

# временная мера для пропуска вещей, с которыми возникают проблемы
# 19 - не открывается страница на сайте
NOT_CHECKING_ITEMS_IDS = [19]


# todo: добавить логирование как у команд бота (начало - конец)
def check_and_order(browser):
    # todo: отвязать от Зары и выбирать скрапер из сайтов в базе
    try:
        for discount_hunter in set(Item.objects.values_list("discount_hunter", flat = True)):
            discount_hunter_items = Item.objects.filter(discount_hunter = discount_hunter)
            for site in set(discount_hunter_items.values_list("site", flat = True)):
                items = [
                    item for item in discount_hunter_items.filter(site = site) if item.id not in NOT_CHECKING_ITEMS_IDS
                ]
                link = DiscountHunterSiteLink.objects.get(discount_hunter = discount_hunter, site = site)
                site_data = SiteData.instances[link.site.name]
                # todo: сначала проверять есть ли вещи для заказа, а потом входить
                log_in(link, site_data, browser)
                clear_basket(site_data, browser)

                ordered_items = {}
                logger.debug(
                    f"{get_user_identification(link.discount_hunter)} - check and order"
                    f" items ids - {sorted([item.id for item in items])}"
                    f" - for {link.site.name} site"
                )
                for item in items:
                    # todo: удалять заказанные вещи из базы (но потом переделать это на выставление вещам поля ordered)
                    need_to_order = True
                    elements_to_find = [ZaraItemInfoScraper.PRICE]
                    if item.has_sizes:
                        if item.sizes:
                            elements_to_find.append(ZaraItemInfoScraper.SIZES_ON_SITE)
                        else:
                            need_to_order = False
                    if item.has_colors:
                        if item.color:
                            elements_to_find.append(ZaraItemInfoScraper.COLORS_ON_SITE)
                        else:
                            need_to_order = False
                    if need_to_order:
                        scraper = ZaraItemInfoScraper(item)
                        scraper.find_elements_on_page(elements_to_find)
                        scraper.init_item(elements_to_find)
                        item.save()
                        if item.current_price <= item.order_price:
                            added_sizes_or_ordered = add_to_basket(site_data, scraper, browser)
                            # todo: переписать проверку и возвращаемые значения из add_to_basket,
                            #  после того, как будет добавлено поле ordered
                            if not item.has_sizes and added_sizes_or_ordered is True \
                                    or item.has_sizes and added_sizes_or_ordered:
                                ordered_items.update({item: added_sizes_or_ordered})

                if ordered_items:
                    check_items_in_basket(ordered_items, site_data, browser)
                    order_all(link, site_data, browser)
                    report_to_discount_hunter(ordered_items, link, site_data, browser)
                    for item in ordered_items:
                        if item.has_sizes:
                            if ordered_items[item]:
                                item.sizes = [size for size in item.sizes if size not in ordered_items[item]]
                                item.save()
                            if not item.sizes:
                                item.delete()
                        else:
                            item.delete()

                log_out(site_data, browser)
    except exceptions_to_restart as error:
        logger.error(msg = f"{type(error)}: {error}: stacktrace:\n{error.stacktrace}")
        # todo: использовать контекст, чтобы обновлять страницу или запускать со следующего шага за сломанным
        # todo: закрывать всплывающий в правом нижнем углу чат, если мешает
        check_and_order(browser)
