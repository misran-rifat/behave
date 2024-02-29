from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def before_all(context):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    context.browser = webdriver.Chrome(options=chrome_options)
    context.browser.implicitly_wait(10)


def after_all(context):
    context.browser.quit()
