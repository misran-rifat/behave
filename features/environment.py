import datetime
import os
import logging
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
import time
import random
from functools import wraps
from typing import Optional, Dict, Any
import json
from pathlib import Path


def retry_on_exception(retries: int = 3, delay: int = 1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == retries - 1:
                        raise
                    time.sleep(delay * (i + 1))
            return None

        return wrapper

    return decorator


class BrowserFactory:
    @staticmethod
    def create_chrome_options(config: Dict[str, Any]) -> ChromeOptions:
        options = ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--log-level=3")

        if config.get("headless", True):
            options.add_argument("--headless")
            options.add_argument(
                f'window-size={config.get("window_size", "2560x1440")}'
            )
        else:
            options.add_argument("--start-maximized")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--verbose")
        options.add_argument("--disable-gpu")
        options.add_argument(
            f"user-agent={config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')}"
        )

        return options

    @staticmethod
    def create_firefox_options(config: Dict[str, Any]) -> FirefoxOptions:
        options = FirefoxOptions()
        if config.get("headless", True):
            options.add_argument("--headless")
        return options

    @staticmethod
    def create_edge_options(config: Dict[str, Any]) -> EdgeOptions:
        options = EdgeOptions()
        if config.get("headless", True):
            options.add_argument("--headless")
        return options

    @staticmethod
    def create_safari_options(config: Dict[str, Any]) -> SafariOptions:
        return SafariOptions()

    @staticmethod
    def create_browser(config: Dict[str, Any]) -> WebDriver:
        browser_type = config.get("browser", "chrome").lower()
        remote_url = config.get("remote_url")

        options_map = {
            "chrome": BrowserFactory.create_chrome_options,
            "firefox": BrowserFactory.create_firefox_options,
            "edge": BrowserFactory.create_edge_options,
            "safari": BrowserFactory.create_safari_options,
        }

        if browser_type not in options_map:
            raise ValueError(f"Unsupported browser: {browser_type}")

        options = options_map[browser_type](config)

        if remote_url:
            return webdriver.Remote(command_executor=remote_url, options=options)

        driver_map = {
            "chrome": webdriver.Chrome,
            "firefox": webdriver.Firefox,
            "edge": webdriver.Edge,
            "safari": webdriver.Safari,
        }

        return driver_map[browser_type](options=options)


class TestContext:
    def __init__(self):
        self.config = self._load_config()
        self.browser: Optional[WebDriver] = None
        self.logger = self._setup_logger()
        self.scenario_data = {}

    @staticmethod
    def _load_config() -> Dict[str, Any]:
        config_path = Path("config.yml")
        if not config_path.exists():
            raise FileNotFoundError("config.yml not found")

        with open(config_path, "r") as file:
            return yaml.safe_load(file)

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("behave")
        logger.setLevel(logging.INFO)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%I:%M:%S %p"
        )
        console_handler.setFormatter(console_formatter)

        # File Handler
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(
            log_dir
            / f"test_run_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    def take_screenshot(self, scenario_name: str, status: str) -> None:
        if not self.browser:
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshots_dir = Path("util/data/screenshots")
        screenshots_dir.mkdir(parents=True, exist_ok=True)

        screenshot_path = (
            screenshots_dir
            / f"{status}_{scenario_name.replace(' ', '_')}_{timestamp}.png"
        )

        try:
            self.browser.save_screenshot(str(screenshot_path))
            self.logger.info(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")


def before_all(context):
    context.test_context = TestContext()
    context.logger = context.test_context.logger
    context.logger.info("Automated testing started")


def after_all(context):
    context.logger.info("Testing completed")


def before_scenario(context, scenario):
    context.logger.info(f"Starting scenario: {scenario.name}")
    context.scenario = scenario
    context.test_context.scenario_data.clear()


def after_scenario(context, scenario):
    if scenario.status == "failed":
        context.test_context.take_screenshot(scenario.name, "failed")
        context.logger.error(f"Scenario failed: {scenario.name}")

        # Log additional debug information
        if hasattr(context, "browser"):
            try:
                context.logger.debug(f"Current URL: {context.browser.current_url}")
                context.logger.debug(
                    f"Page source length: {len(context.browser.page_source)}"
                )
            except WebDriverException:
                context.logger.debug("Could not retrieve browser information")

    context.logger.info(
        f"Completed scenario: {scenario.name} - Status: {scenario.status}"
    )


@retry_on_exception(retries=3, delay=2)
def before_tag(context, tag):
    if tag == "ui":
        try:
            context.browser = BrowserFactory.create_browser(context.test_context.config)
            context.browser.implicitly_wait(
                context.test_context.config.get("implicit_wait", 30)
            )
            context.browser.set_page_load_timeout(
                context.test_context.config.get("page_load_timeout", 30)
            )

            if isinstance(context.browser, webdriver.Chrome):
                context.browser.execute_cdp_cmd(
                    "Page.addScriptToEvaluateOnNewDocument",
                    {
                        "source": """
                            Object.defineProperty(navigator, 'webdriver', {
                                get: () => undefined
                            })
                        """
                    },
                )

            context.logger.info(
                f"Started {context.test_context.config.get('browser', 'chrome')} browser"
            )
        except Exception as e:
            context.logger.error(f"Failed to start browser: {str(e)}")
            raise


def after_tag(context, tag):
    if tag == "ui" and hasattr(context, "browser"):
        try:
            context.browser.quit()
            context.logger.info("Browser closed successfully")
        except Exception as e:
            context.logger.error(f"Error closing browser: {str(e)}")
        finally:
            context.browser = None
