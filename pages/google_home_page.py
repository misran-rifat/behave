from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class SearchPage:
    def __init__(self, browser):
        self.browser = browser
        self.search_bar_xpath = "//textarea[@name='q']"

    def go_to(self, url):
        self.browser.get(url)

    def search_for(self, search_word):
        search_bar = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, self.search_bar_xpath)))
        assert search_bar.is_displayed(), "The search bar is not visible."
        search_bar.send_keys(search_word + Keys.ENTER)

    def title_should_contain(self, search_word):
        WebDriverWait(self.browser, 10).until(EC.title_contains(search_word))
        assert search_word in self.browser.title, f"The page title does not contain {search_word}"
