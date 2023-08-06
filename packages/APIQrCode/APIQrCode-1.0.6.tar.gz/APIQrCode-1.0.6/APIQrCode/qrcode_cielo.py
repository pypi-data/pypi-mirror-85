from .request.get_access_token import GetAccessToken
from .request.get_public_key import GetPublicKey
from .request.parse_qrcode import ParseQRCode
from .request.payment_card import PaymentCard


class QrCodeCielo:
    _client_id: str = None
    _client_secret: str = None
    _sandbox: bool = None

    def __init__(self, client_id: str, client_secret: str, sandbox: bool = False):
        self._client_id = client_id
        self._client_secret = client_secret
        self._sandbox = sandbox

    def get_access_token(self) -> dict:
        request = GetAccessToken.execute(
            client_id=self._client_id, client_secret=self._client_secret, sandbox=self._sandbox)
        return request

    def get_public_key(self, access_token: str) -> dict:
        request = GetPublicKey.execute(access_token=access_token, sandbox=self._sandbox)
        return request

    def payment_card(self, access_token: str, data: dict) -> dict:
        request = PaymentCard.execute(
            access_token=access_token, data=data, sandbox=self._sandbox)
        return request

    def parse_qrcode(self, access_token: str, qrcode: str) -> dict:
        request = ParseQRCode.execute(
            access_token=access_token, qrcode=qrcode, sandbox=self._sandbox)
        return request
