import logging
import os

import pytest

from ui.entities.user import User
from ui.enums.registration_controls_texts import RegistrationControlsTexts
from ui.enums.urls import URLS
from ui.pages.web_trading_page import WebTradingPage
from ui.tests.conftest import driver, logger
from ui.pages.home_page import HomePage
from ui.enums.registration_buttons import RegistrationButtons
from ui.pages.registration_page import RegistrationPage
from selenium.webdriver.chrome.webdriver import WebDriver
from helpers.test_data_helpers import (make_test_data_unique,
                                       get_test_data_from_json)


data_registration: dict = get_test_data_from_json(os.path.join(
    os.path.dirname(__file__),
    "test_registration_data_user.json"))


@pytest.mark.order(1)
@pytest.mark.parametrize("test_case",
                         data_registration,
                         ids=[data["test_case_title"]
                              for data in data_registration])
def test_registration(driver: WebDriver, test_case: dict):
    driver.get(URLS.REGISTRATION_PAGE.value)

    test_case["data"]["email"] = make_test_data_unique(
        test_case["data"]["email"])
    user = User(**test_case["data"])
    registration_page: RegistrationPage = RegistrationPage(driver)

    web_trading_page: WebTradingPage = (registration_page
                                        .fill_form_success(driver, user))
    web_trading_page.wait_welcome_dialog()
    assert web_trading_page.driver.current_url == URLS.WEB_TRADING_PAGE, \
        (f'Expected WebTradingPage, but was '
         f'{web_trading_page.driver.current_url}.')


data_pwd_controls: dict = get_test_data_from_json(os.path.join(
    os.path.dirname(__file__),
    "test_registration_data_pwd_controls.json"))


@pytest.mark.order(2)
@pytest.mark.parametrize("test_case",
                         data_pwd_controls,
                         ids=[data["test_case_title"]
                              for data in data_pwd_controls])
def test_registration_form_password_controls(
        driver: WebDriver, test_case: dict):
    logging.info('Go to the RegistrationPage')
    driver.get(URLS.REGISTRATION_PAGE.value)

    logging.info(f'Create user from test data {test_case["data"]}')
    user = User(**test_case["data"])

    registration_page: RegistrationPage = RegistrationPage(driver)
    logging.info('Fill registration page')
    registration_page: RegistrationPage = (registration_page
                                           .fill_form_failure(driver, user))

    logging.info('Check if registration is not completed '
                 'and we are still on the RegistrationPage')
    assert registration_page.url_contains(URLS.REGISTRATION_PAGE.value), \
        f'Expected RegistrationPage, but was {driver.current_url}'

    for control in test_case["controlColor"]:
        expected_color = test_case["controlColor"][control]
        control_text: str = RegistrationControlsTexts[control].value
        logging.info(f"Get color of the control text '{control_text}'")
        control_text_color: str = (registration_page.get_control_color(
            registration_page, control_text))
        logging.info('Check if color is correct')
        assert control_text_color == expected_color, \
            f'Expected {expected_color} color, but was {control_text_color}'


@pytest.mark.order(3)
@pytest.mark.parametrize("btn", list(RegistrationButtons))
def test_registration_buttons(driver: WebDriver, btn: RegistrationButtons):
    driver.get(URLS.HOME_PAGE.value)
    home_page: HomePage = HomePage(driver)

    logger.info(f'Go to the Registration page by clicking {btn}')
    registration_page: RegistrationPage = (
        home_page.go_to_registration_page(driver, btn.value))

    logger.info('Check if title is correct')
    assert registration_page.is_title_correct()

    logger.info('Check if url of RegistrationPage is correct')
    assert registration_page.url_contains(URLS.REGISTRATION_PAGE.value), \
        f'Expected RegistrationPage, but was {driver.current_url}'

    logger.info('Check if header of registration form is correct')
    assert registration_page.is_header_located()
