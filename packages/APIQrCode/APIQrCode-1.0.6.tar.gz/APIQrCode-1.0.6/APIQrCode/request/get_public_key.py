import requests

from APIQrCode.constants import ServiceURLS
from APIQrCode.environment import Environment
from .error import Error


class GetPublicKey:
    @classmethod
    def execute(cls, access_token: str, sandbox: bool = False) -> dict:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        environment = Environment(sandbox=sandbox)

        url = f'{environment.base_url}{ServiceURLS.public_key}'

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return {
                'status_code': response.status_code,
                'public_key': response.json()['public_key'],
                'key_id': response.json()['key_id'],
                'expires_in': response.json()['expires_in']
            }

        return Error.process(response.status_code, response)
