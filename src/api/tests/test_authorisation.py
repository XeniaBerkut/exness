import pytest
import requests

from api.entities.user import User
from api.enums.endpoints.auth import AuthEndpoints
from api.tests.conftest import faulty_authorisation_data
from src.helpers.logger import Logger

logger = Logger(logging_level='DEBUG')


@pytest.mark.order(1)
def test_token_get_validation(partner_token, headers_fixture):
    logger.info("Set header")
    headers: dict = headers_fixture
    headers["Authorization"] = partner_token

    logger.info("Get auth request")
    response = requests.get(
        AuthEndpoints.TOKEN.value,
        headers=headers
    )

    logger.info("Check if status_code is correct")
    assert response.status_code == 200, \
        f'Expected status code 200, but was {response.status_code}.'


@pytest.mark.order(1)
def test_token_post_validation(partner_token, headers_fixture):
    logger.info("Set header")
    headers: dict = headers_fixture
    headers["Authorization"] = partner_token
    logger.info("Get auth request")
    response = requests.get(
        AuthEndpoints.TOKEN.value,
        headers=headers
    )
    logger.info("Check if status_code is correct")
    assert response.status_code == 200, \
        f'Expected status code 200, but was {response.status_code}.'


@pytest.mark.order(2)
def test_token_post_unauthorized(headers_fixture):
    logger.info("Set header")

    logger.info("Get auth request")
    response = requests.get(
        AuthEndpoints.TOKEN.value,
        headers=headers_fixture
    )
    logger.info("Check if status_code is correct")
    assert response.status_code == 401, \
        f'Expected status code 401, but was {response.status_code}.'


@pytest.mark.order(2)
def test_token_post_bad_request(partner_token, headers_fixture):
    logger.info("Set header")
    headers: dict = headers_fixture
    headers["Authorization"] = partner_token
    headers["Bad Request"] = '$#@^&*('

    logger.info("Get auth request")
    response = requests.get(
        AuthEndpoints.TOKEN.value,
        headers=headers
    )
    logger.info("Check if status_code is correct")
    assert response.status_code == 400, \
        f'Expected status code 400, but was {response.status_code}.'


@pytest.mark.order(2)
def test_token_deletion(partner_token, headers_fixture):
    logger.info("Set header")
    headers: dict = headers_fixture
    headers["Authorization"] = partner_token
    logger.info("Delete token")
    response = requests.delete(
        AuthEndpoints.TOKEN.value,
        headers=headers
    )
    logger.info("Check if status_code is correct")
    assert response.status_code == 200, \
        f'Expected status code 200, but was {response.status_code}.'

    logger.info("Check deleted token")
    response = requests.get(
        AuthEndpoints.TOKEN.value,
        headers=headers
    )
    logger.info("Check if status_code is correct")
    assert response.status_code == 401, \
        f'Expected status code 401, but was {response.status_code}.'


data_auth_fail: list = faulty_authorisation_data()


@pytest.mark.order(2)
@pytest.mark.parametrize("test_case",
                         data_auth_fail,
                         ids=[data["test_case_title"]
                              for data in data_auth_fail])
def test_authorisation_faulty(headers_fixture, test_case: dict):
    logger.info("Set header and body")
    user = User(**test_case["data"])

    logger.info("Request authorisation")
    response = requests.post(
        AuthEndpoints.AUTH.value,
        headers=headers_fixture,
        data=user.to_json()
    )
    logger.debug(f"Print response {response.json()}")
    logger.info("Check if status_code is correct")
    assert response.status_code == test_case["expected_response"], \
        (f'Expected {test_case["expected_response"]}, '
         f'but was {response.status_code}')
