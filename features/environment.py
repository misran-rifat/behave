import datetime
import os
import logging
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


def before_all(context):
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%I:%M:%S %p')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    context.logger = logger
    context.logger.info('Automated testing started')


def after_all(context):
    context.logger.info(f'Testing is completed.')


def before_scenario(context, scenario):
    context.logger.info(f'Scenario: {scenario.name}')


def after_scenario(context, scenario):
    if scenario.status == "failed":
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join("util", "data", "screenshots", f"failed_{scenario.name.replace(' ', '_')}_{timestamp}.png")
        context.browser.save_screenshot(screenshot_path)


def before_tag(context, tag):
    if tag == "ui":
        context.logger.info(f"Tag : {tag}")
        with open('config.yml', 'r') as file:
            config = yaml.safe_load(file)
        browser_type = config.get('browser', 'chrome').lower()

        if browser_type == 'chrome':
            options = ChromeOptions()
            options.add_argument("--disable-blink-features")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--log-level=3")
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument('window-size=2560x1440')
            options.add_argument("--verbose")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
            options.add_argument('--disable-gpu')
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

        context.logger.info(f"Starting browser : {browser_type}")
        context.browser.implicitly_wait(10)
        context.browser.set_page_load_timeout(10)


def after_tag(context, tag):
    if tag == "ui":
        context.logger.info(f"Tag : {tag}")
        context.browser.quit()
        context.logger.info(f'Browser closed')
