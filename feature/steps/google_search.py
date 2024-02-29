from behave import *
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@given("user visits {url}")
def step_impl(context, url):
    context.browser.get(url)


@then("user searches {search_word}")
def step_impl(context, search_word):
    search_bar = WebDriverWait(context.browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//textarea[@name='q']")))
    assert search_bar.is_displayed(), "The search bar is not visible."
    search_bar.send_keys(search_word + Keys.ENTER)


@then("the page title should contain the {search_word}")
def step_impl(context, search_word):
    WebDriverWait(context.browser, 10).until(EC.title_contains(search_word))
    assert search_word in context.browser.title
