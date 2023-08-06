from APIQrCode.environment import Environment
from APIQrCode.constants import BaseURLS


def test_environment_sandbox():
    environment = Environment(sandbox=True)
    assert environment.sandbox
    assert environment.base_url == BaseURLS.sandbox


def test_environment_production():
    environment = Environment(sandbox=False)
    assert not environment.sandbox
    assert environment.base_url == BaseURLS.production
