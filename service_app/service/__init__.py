from discount_waiter.settings import BASE_DIR
from service_app.constants import USER_AGENT
from selenium import webdriver
import platform


# https://peter.sh/experiments/chromium-command-line-switches/
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={USER_AGENT}")
# todo: запускать с headless, должно работать быстрее
#  (сейчас, при запуске с этим параметром, возникают проблемы с поиском элементов)
# options.add_argument("headless")
# options.add_argument("window-size=1920,1080")

# параметры для просмотра человеком
options.add_argument("start-maximized")
# options.add_argument("auto-open-devtools-for-tabs")

browser = webdriver.Chrome(executable_path = f"{BASE_DIR}/chromedriver.exe", options = options)


def get_platform():
    return platform.node()


def update_model_instance(model, model_instance, filters):
    update_data = model_instance.__dict__.copy()
    del update_data["_state"]
    del update_data["id"]
    return model.objects.filter(**filters).update(**update_data)
