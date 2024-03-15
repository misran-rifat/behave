from selenium.webdriver import Keys

from util.ui import *


class SearchPage:
    search_bar_xpath = "//textarea[@name='q']"

    def __init__(self, browser):
        self.browser = browser

    def go_to(self, url):
        self.browser.get(url)

    def search_for(self, search_word):
        search_bar = wait_for_element_visibility_using_xpath(self.browser, SearchPage.search_bar_xpath)
        assert search_bar.is_displayed(), f"{search_bar} is not visible."
        search_bar.send_keys(search_word + Keys.ENTER)

    def title_should_contain(self, search_word):
        wait_for_title_contains(self.browser, search_word)
        assert search_word in self.browser.title, f"The page title does not contain {search_word}"
