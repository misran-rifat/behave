from behave import *
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


@given("user visits {url}")
def step_impl(context, url):
    context.browser.get(url)


@then("user searches {search_word}")
def step_impl(context, search_word):
    search_bar = context.browser.find_element(By.XPATH, "//textarea[@name='q']")
    search_bar.send_keys(search_word + Keys.ENTER)


@then("the page title should contain the {search_word}")
def step_impl(context, search_word):
    assert context.browser.title.__contains__(search_word), f"Title does not contain {search_word}"
