from selenium.webdriver.common.by import By
from ui.pages.base_page import BasePage


class WebTradingPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    locators = {
        'welcome_dialog': (By.XPATH, '//div[@data-test="welcome-dialog"]')
    }

    def wait_welcome_dialog(self):
        self.wait_element_is_interactable(
            self.locators['welcome_dialog'], timeout=20)
