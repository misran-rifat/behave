from behave import *

from feature.pages.search_page import SearchPage


@given("user visits {url}")
def step_impl(context, url):
    context.search_page = SearchPage(context.browser)
    context.search_page.go_to(url)


@then("user searches {search_word}")
def step_impl(context, search_word):
    context.search_page.search_for(search_word)


@then("the page title should contain the {search_word}")
def step_impl(context, search_word):
    context.search_page.title_should_contain(search_word)
