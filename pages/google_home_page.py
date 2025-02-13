from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Keys

from util.ui import *


class SearchPage:
    search_bar_xpath = "//textarea[@name='q']"

    def __init__(self, browser):
        self.browser = browser

    def go_to(self, url):
        try:
            self.browser.get(url)
        except TimeoutException:
            raise TimeoutException(f"Timeout while loading URL: {url}")

    def search_for(self, search_word):
        try:
            search_bar = wait_for_element_visibility_using_xpath(self.browser, SearchPage.search_bar_xpath)
            assert search_bar.is_displayed(), f"{search_bar} is not visible."
            search_bar.send_keys(search_word + Keys.ENTER)
        except TimeoutException:
            raise TimeoutException(f"Search bar element not found within timeout period")

    def title_should_contain(self, search_word):
        try:
            wait_for_title_contains(self.browser, search_word)
            assert search_word in self.browser.title, f"The page title does not contain {search_word}"
        except TimeoutException:
            raise TimeoutException(f"Title did not contain '{search_word}' within timeout period")
