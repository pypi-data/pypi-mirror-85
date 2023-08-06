import base64
import json

import requests

from APIQrCode.constants import ServiceURLS
from APIQrCode.environment import Environment
from .error import Error


def _encodeBase64(message) -> str:
    message_bytes = message.encode('ascii')
    base_64_bytes = base64.b64encode(message_bytes)
    return base_64_bytes.decode('ascii')


class GetAccessToken:

    @classmethod
    def execute(cls, client_id: str, client_secret: str, sandbox: bool = False) -> dict:
        message_to_encode = f'{client_id}:{client_secret}'
        authorization_basic = f'Basic {_encodeBase64(message_to_encode)}'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': authorization_basic
        }

        body = {
            "grant_type": "client_credentials",
        }

        environment = Environment(sandbox=sandbox)

        url = f'{environment.base_url}{ServiceURLS.access_token}'

        response = requests.post(url, headers=headers, data=json.dumps(body))

        if response.status_code == 201:
            return {
                'status_code': response.status_code,
                'access_token': response.json()['access_token'],
                'expires_in': response.json()['expires_in']
            }

        return Error.process(response.status_code, response)
