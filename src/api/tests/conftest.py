import os
import pytest

from api.endpoints.auth.token import Token
from api.entities.user import User
from helpers.test_data_helpers import get_test_data_from_json

secrets_file_path = os.path.join(os.path.dirname(__file__), "secrets.json")


@pytest.fixture()
def partner_token(headers_fixture) -> str:
    partner_user = User(**get_test_data_from_json(secrets_file_path))
    token = Token(partner_user)
    return token.get_token(headers_fixture)


@pytest.fixture()
def headers_fixture() -> dict:
    headers: dict = get_test_data_from_json(os.path.join(
        os.path.dirname(__file__),
        "test_authorisation_data_headers.json"))
    return headers


def faulty_authorisation_data() -> list:
    data = get_test_data_from_json(os.path.join(
        os.path.dirname(__file__),
        "test_authorisation_data_faulty.json"))
    return data
