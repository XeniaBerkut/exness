import logging

from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from ui.entities.user import User
from ui.pages.base_page import BasePage
from ui.pages.web_trading_page import WebTradingPage
from selenium.webdriver.support import expected_conditions as EC


class RegistrationPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    locators = {
        'registration_header': (
            By.XPATH, '//span[contains(text(), "Create an account")]'),
        'country': (By.NAME, "country"),
        'country_control': (By.ID, "mui-2-helper-text"),
        'email': (By.NAME, "email"),
        'email_control': (By.ID, "mui-3-helper-text"),
        'password': (By.NAME, "password"),
        'pwd_control': (By.ID, "mui-4-helper-text"),
        'sing_up_btn': (By.ID, "mui-6"),
        'captcha': (By.ID, "recaptcha-anchor-label")
    }

    def is_title_correct(self, timeout: int = 10) -> bool:
        try:
            (WebDriverWait(self.driver, timeout)
             .until(EC.title_is('Exness Sign Up')))
            return True
        except TimeoutException:
            return False

    def is_header_located(self) -> bool:
        return bool(EC.presence_of_element_located(
            self.locators['registration_header']))

    def select_country_by_typing(self, country: str):
        logging.info('Chose country: {}'.format(country))
        country_field = self.driver.find_element(*self.locators['country'])
        country_field.send_keys(country)
        country_field.send_keys(Keys.RETURN)

    def fill_email(self, email):
        logging.info('Fill email'.format(email))
        self.driver.find_element(*self.locators['email']).send_keys(email)

    def fill_password(self, password):
        logging.info('Fill password')
        (self.driver.find_element(*self.locators['password'])
         .send_keys(password))

    def confirm_registration(self):
        logging.info('Confirm registration')
        self.driver.find_element(*self.locators['sing_up_btn']).click()

    def fill_form(self, user: User):
        self.select_country_by_typing(user.country)
        self.fill_email(user.email)
        self.fill_password(user.password)
        self.confirm_registration()

    def fill_form_success(self, driver: WebDriver,  user: User):
        self.fill_form(user)
        return WebTradingPage(driver)

    def fill_form_failure(self, driver: WebDriver,  user: User):
        self.fill_form(user)
        return RegistrationPage(driver)

    def get_control_color(self, page, control_text: str) -> str:
        logging.info('Get password controls text field')
        pwd_control: WebElement = page.driver.find_element(
            *self.locators['pwd_control'])
        logging.info(f'Get password control "{control_text}" field')
        control_text_element_xpath: str = (f'//span[contains(text(),'
                                           f'"{control_text}")]')
        control_string: WebElement = pwd_control.find_element(
            By.XPATH, control_text_element_xpath)
        logging.info('Get color of the text')
        return control_string.value_of_css_property("color")
