from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

time_out = 30


def wait_for_element_visibility_using_xpath(browser, xpath, timeout=time_out):
    return WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))


def wait_for_title_contains(browser, search_word, timeout=time_out):
    return WebDriverWait(browser, timeout).until(EC.title_contains(search_word))
