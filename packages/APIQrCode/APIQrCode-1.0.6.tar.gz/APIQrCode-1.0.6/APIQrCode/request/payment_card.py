import json

import requests

from APIQrCode.constants import ServiceURLS
from APIQrCode.environment import Environment
from .error import Error
from .rsa_cryptography import RSACryptography


class PaymentCard:
    @classmethod
    def execute(cls, access_token: str, data: dict, sandbox: bool = False) -> dict:
        public_key = data.get('public_key')
        data_to_encrypt = data.get('card_data')
        data_to_encrypt = json.dumps(data_to_encrypt)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }
        payload = {
            'key_id': data.get('key_id'),
            'payee_document': data.get('payee_document'),
            'qrcode': data.get('qrcode'),
            'card_data': RSACryptography.encrypt(data_to_encrypt, public_key)
        }

        environment = Environment(sandbox=sandbox)
        url = f'{environment.base_url}{ServiceURLS.payment_card}'

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            return {
                'status_code': response.status_code,
                'reference_label': response.json()['reference_label'],
                'merchant_id': response.json()['merchant_id'],
                'terminal_id': response.json()['terminal_id'],
                'authorization_code': response.json()['authorization_code'],
                'authentication_code': response.json()['authentication_code'],
                'host_nsu': response.json()['host_nsu'],
                'terminal_nsu': response.json()['terminal_nsu'],
                'timestamp': response.json()['timestamp'],
                'card_scheme': response.json()['card_scheme'],
            }

        return Error.process(response.status_code, response)
