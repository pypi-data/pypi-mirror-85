from base64 import b64decode, b64encode

from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.PublicKey import RSA


class RSACryptography:
    @classmethod
    def encrypt(cls, message: str, public_key: str) -> str:
        keyDER = b64decode(public_key)
        KeyPub = RSA.importKey(keyDER)
        cipher = Cipher_PKCS1_v1_5.new(KeyPub)
        cipher_text = cipher.encrypt(message.encode())
        encode_msg = b64encode(cipher_text)
        return encode_msg.decode()
