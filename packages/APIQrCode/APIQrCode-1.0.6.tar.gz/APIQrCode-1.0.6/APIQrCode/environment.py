from APIQrCode.constants import BaseURLS


class Environment:
    base_url: str
    sandbox: bool = False

    def __init__(self, sandbox: bool):
        if not sandbox:
            self.base_url = BaseURLS.production
        else:
            self.sandbox = True
            self.base_url = BaseURLS.sandbox
