<div style="text-align:center"><img width="300px" src="doc/jeitto.svg" /></div>

# APIQrCode

SDK QrCode Cielo


## Requisitos:
- Python 3.x

## Uso:

- Instalação:

``pip install APIQrCode``

- Exemplo:
```python
from APIQrCode.qrcode_cielo import QrCodeCielo

  
qrcode_cielo = QrCodeCielo(client_id='your client id', client_secret='your client secret', sandbox=True)

# get access token data
access_token_data = qrcode_cielo.get_access_token()
access_token = access_token_data.get('access_token')
print(f'Access token data : {access_token_data}')

# parse qrcode
parse_qrcode = qrcode_cielo.parse_qrcode(access_token=access_token, qrcode='your qrcode')
print(f'Parse QRCode: {parse_qrcode}')

# get public key data
public_key_data = qrcode_cielo.get_public_key(access_token=access_token)
print(f'Public Key: {public_key_data}')

# process payment
public_key = public_key_data.get('public_key')
public_key_id = public_key_data.get('key_id')

card_data = {
    'card_number': '5496228363201473',
    'card_cvv': '128',
    'card_holder_name': 'JOAO DA SILVA',
    'card_expiration_date': '0225'
}
data = {
    'key_id': public_key_id,
    'payee_document': '78362896051',
    'qrcode': 'qrcode',
    'card_data': card_data,
    'public_key': public_key
}

payment_card = qrcode_cielo.payment_card(access_token=access_token, data=data)
print(f'Payment card: {payment_card}')

```

- Exemplo completo em: ```/example/qr_code_cielo.py```