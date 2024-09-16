import logging

from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage
from ui.pages.registration_page import RegistrationPage

logger = logging.getLogger()


class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    locators = {
        'sign_up_btn_menu': (By.XPATH, "//a[contains(@data-param, 'menu') "
                                       "and @data-testid='button:sign-up']"),
        'sign_up_btn_header': (By.XPATH, '//a[contains(@data-param, "header") '
                                         'and @data-testid="button:sign-up"]'),
        'sign_up_btn_bottom': (By.XPATH, '//a[contains(@data-param, "bottom") '
                                         'and @data-testid="button:sign-up"]')
    }

    def go_to_registration_page(self, driver, registration_btn: str):
        logger.info(f'Click registration button {registration_btn}')
        registration_button = self.driver.find_element(
            *self.locators[registration_btn])
        registration_button.click()
        logger.info('The registration button was clicked')

        logger.info('Check if there are only two active pages')
        # TODO use number_of_windows_to_be from EC
        expected_active_pages_count: int = 2
        active_pages: list[str] = driver.window_handles
        registration_page: str = active_pages[1]

        assert len(active_pages) == expected_active_pages_count, \
            (f'Expected {expected_active_pages_count} active pages, '
             f'but was {len(active_pages)}')

        logger.info("Check if HomePage is still active")
        assert driver.current_url == 'https://www.exness.com/', \
            f'Expected HomePage is active, but was {driver.current_url}'

        logger.info('Switch to RegistrationPage')
        driver.switch_to.window(registration_page)
        return RegistrationPage(driver)
