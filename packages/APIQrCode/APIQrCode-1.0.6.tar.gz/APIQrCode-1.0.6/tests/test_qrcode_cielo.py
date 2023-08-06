from APIQrCode.qrcode_cielo import QrCodeCielo

PUBLIC_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsZXFpk5LUOiHEZIT5+PVGXRP2Qj/rxdvp7WCDoX' \
             'ZndLoIZBzKooTXLvNk3bp8MlLXEWPci8KfhesAo6edAiWPGTNgLGU8cyxybSWGILV9wms4rBcLpb0siFyvc' \
             '1iHNhVRYgwdsf6Qreb8xWo7uKLu0tMQwtPaJVmG/A95T57Tht/jcweD7kIUz80CkVBnTIxSFULDwXItghVU' \
             'hsTxU9RfE7jz3W/el+N8L1R/eHVkt9tmufORmQlDdngJSZeS/pT572XgcZJ0HheFtEf+AxBvdQPt984lnvA' \
             'OCEOBHhlU8SAAqjkBaR5vKj2JIIku/gkb1aIb3PNHfIDT7TvHyPlFQIDAQAB'


def test_get_access_token(mocker):
    expected_result = {
        'status_code': 200,
        'access_token': '36751ddd-21ec-3182-850e-89894ab08bab',
        'expires_in': 86400
    }
    mock = mocker.patch(
        'APIQrCode.request.get_access_token.GetAccessToken.execute',
        return_value=expected_result
    )
    qrcode_cielo = QrCodeCielo('', '', True)
    result = qrcode_cielo.get_access_token()

    assert mock.called
    assert result == expected_result


def test_get_public_key(mocker):
    expected_result = {
        'status_code': 200,
        'public_key': PUBLIC_KEY,
        'key_id': '1b59934a-7eaa-4f90-a391-585de0ffc550',
        'expires_in': 43604
    }

    mock = mocker.patch(
        'APIQrCode.request.get_public_key.GetPublicKey.execute',
        return_value=expected_result
    )
    qrcode_cielo = QrCodeCielo('', '', True)
    result = qrcode_cielo.get_public_key('')

    assert mock.called
    assert result == expected_result


def test_payment_card(mocker):
    expected_result = {
        'status_code': 200,
        'reference_label': 'test',
        'merchant_id': 'test',
        'terminal_id': 'test',
        'authorization_code': 'test',
        'authentication_code': 'test',
        'host_nsu': 'test',
        'terminal_nsu': 'test',
        'timestamp': 'test',
        'card_scheme': 'test',
    }

    mock = mocker.patch(
        'APIQrCode.request.payment_card.PaymentCard.execute',
        return_value=expected_result
    )

    data = {
        'key_id': '123a',
        'payee_document': '00000000000',
        'qrcode': '010101010101010',
        'card_data': {
            'card_number': '1312321',
            'card_holder_name': 'test',
            'card_expiration_date': '0222'
        },
        'public_key': PUBLIC_KEY
    }

    qrcode_cielo = QrCodeCielo('', '', True)
    result = qrcode_cielo.payment_card(access_token='', data=data)

    assert mock.called
    assert result == expected_result


def test_parse_qrcode(mocker):
    expected_result = {
        'status_code': 200,
        'qrcode_data': {
            "payload_format_indicator": "01",
            "point_of_initiation_method": "12",
            "merchant_account_information": {
                "gui": "br.com.padraoq",
                "id_merchant": "0010000244470001",
                "id_terminal": "62000092",
                "id_credenciador": "0001"
            },
            "merchant_category_code": "0300",
            "transaction_currency": "986",
            "transaction_amount": "123.99",
            "country_code": "BR",
            "merchant_name": "POSTO_ABC",
            "merchant_city": "Barueri_SP",
            "additional_data_field": {
                "reference_label": "1000230716416292"
            },
            "crc16": "1213",
            "payment_information": {
                "gui": "br.com.padraoq",
                "timestamp": "230120171643",
                "modalidade": "0004",
                "parcelas": "02",
                "tipo_de_transacao": "01",
                "fonte_de_dados_do_pagamento": "03"
            }
        }
    }

    mock = mocker.patch(
        'APIQrCode.request.parse_qrcode.ParseQRCode.execute',
        return_value=expected_result
    )

    qrcode_cielo = QrCodeCielo('', '', True)
    result = qrcode_cielo.parse_qrcode(access_token='', qrcode='')

    assert mock.called
    assert result == expected_result
