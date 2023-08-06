from APIQrCode.constants import BaseURLS, ServiceURLS


def test_base_urls_exists():
    assert BaseURLS.production
    assert BaseURLS.sandbox


def test_service_urls_exists():
    assert ServiceURLS.access_token
    assert ServiceURLS.public_key
    assert ServiceURLS.parse_qrcode
    assert ServiceURLS.payment_card
