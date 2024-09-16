import requests

from api.entities.user import User
from api.enums.endpoints.auth import AuthEndpoints
from requests import Response

from src.helpers.logger import Logger

logger = Logger(logging_level='INFO')


class Token:
    def __init__(self, user: User):
        super().__init__()
        self.user = user

    def get_token(self, headers: dict) -> str:
        logger.info("Prepare request to get token")
        body = self.user.to_json()
        logger.info("Request token with secret data(login & password")
        response: Response = requests.post(
            AuthEndpoints.AUTH.value,
            headers=headers,
            data=body
        )
        logger.debug(f"Print response {response.json()}")
        assert response.status_code == 200, \
            f'Expected status code 200, but was {response.status_code}'
        logger.info(f"Collect response message")
        response_body: dict = response.json()
        logger.info("Return token")
        token_prefix = "JWT "
        token = token_prefix + response_body["token"]
        return token
