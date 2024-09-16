import logging

from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver: WebDriver):
        super().__init__()
        self.driver = driver

    def wait_element_is_interactable(self, locator: tuple, timeout: int):
        logging.info(f"Wait for {locator} to be visible and clickable")
        (WebDriverWait(self.driver, timeout)
         .until(EC.presence_of_element_located(locator)))
        (WebDriverWait(self.driver, timeout)
         .until(EC.element_to_be_clickable(locator)))
        logging.info("Element is clickable")

    def url_contains(self, expected_url: str, timeout: int = 10) -> bool:
        try:
            (WebDriverWait(self.driver, timeout)
             .until(EC.url_contains(expected_url)))
            return True
        except TimeoutException:
            return False
