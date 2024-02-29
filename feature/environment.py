import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import os


def before_all(context):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_dir, '..', 'config.yml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    browser_type = config.get('browser', 'chrome').lower()

    if browser_type == 'chrome':
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("window-size=2560x1440")
        options.add_argument("--log-level=3")
        context.browser = webdriver.Chrome(options=options)

    elif browser_type == 'firefox':
        context.browser = webdriver.Firefox()
        context.browser.maximize_window()

    elif browser_type == 'edge':
        options = EdgeOptions()
        options.add_argument("--headless")
        context.browser = webdriver.Edge(options=options)

    elif browser_type == 'safari':
        context.browser = webdriver.Safari()

    elif browser_type == 'ie':
        context.browser = webdriver.Ie()

    else:
        raise ValueError(f"Unsupported browser: {browser_type}")

    context.browser.implicitly_wait(10)
    context.browser.set_page_load_timeout(10)


def after_all(context):
    context.browser.quit()
