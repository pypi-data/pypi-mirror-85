import requests

from APIQrCode.constants import ServiceURLS
from APIQrCode.environment import Environment
from .error import Error


class ParseQRCode:
    @classmethod
    def execute(cls, access_token: str, qrcode: str, sandbox: bool = False) -> dict:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        environment = Environment(sandbox=sandbox)

        url = f'{environment.base_url}{ServiceURLS.parse_qrcode}'
        params = {'qrcode': qrcode}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return {
                'status_code': response.status_code,
                'qrcode_data': response.json()['qrcode_data']
            }

        return Error.process(response.status_code, response)
