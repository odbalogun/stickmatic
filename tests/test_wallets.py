import json
from app.models import Wallet


def test_retrieve_wallets(client, init_database):
    response = client.get('/api/wallets')

    assert response.status_code == 200
    data = response.json
    assert len(data) == 2


def test_fetch_single_wallet(client, init_database):
    wallet = Wallet.query.get(1)

    response = client.get(f'/api/wallets/{wallet.id}')
    assert response.status_code == 200
    data_1 = response.json
    assert wallet.id == data_1.get('id')
    assert wallet.uuid == data_1.get('uuid')

    response = client.get(f'/api/wallets/{wallet.uuid}')
    assert response.status_code == 200
    data_2 = response.json
    assert wallet.id == data_2.get('id')
    assert wallet.uuid == data_2.get('uuid')


def test_that_money_can_be_deposited_in_wallet(client, init_database):
    wallet = Wallet.query.get(1)

    payload = {'amount': 3000, 'mode': "paystack"}
    response = client.post(f'/api/wallets/{wallet.id}/deposit', data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json
    assert wallet.id == data.get('id')
    assert data.get('balance') == wallet.balance
    assert len(data.get('funding_history')) == len(wallet.funding_history)


def test_for_incomplete_deposit_information(client, init_database):
    wallet = Wallet.query.get(1)

    payload = {'mode': "paystack"}
    response = client.post(f'/api/wallets/{wallet.id}/deposit', data=json.dumps(payload))
    assert response.status_code == 400

    payload = {'amount': 3000}
    response = client.post(f'/api/wallets/{wallet.id}/deposit', data=json.dumps(payload))
    assert response.status_code == 400


def test_for_successful_purchase(client, init_database):
    wallet = Wallet.query.get(1)

    # fund wallet
    payload = {'amount': 20000, 'mode': "paystack"}
    client.post(f'/api/wallets/{wallet.id}/deposit', data=json.dumps(payload))

    # make purchase
    payload = {'price': 10000, 'products': "1, 2, 4, 10, 99"}
    response = client.post(f'/api/wallets/{wallet.id}/purchase', data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json
    assert wallet.id == data.get('id')
    assert data.get('balance') == wallet.balance
    assert len(data.get('purchase_history')) == len(wallet.purchase_history)


def test_for_insufficient_funds(client, init_database):
    wallet = Wallet.query.get(1)

    # make purchase
    payload = {'price': 1000000, 'products': "1, 2, 4, 10, 99"}
    response = client.post(f'/api/wallets/{wallet.id}/purchase', data=json.dumps(payload))
    assert response.status_code == 400


def test_for_invalid_data(client, init_database):
    wallet = Wallet.query.get(1)

    # make purchase
    payload = {'price': 10000}
    response = client.post(f'/api/wallets/{wallet.id}/purchase', data=json.dumps(payload))
    assert response.status_code == 400

    payload = {'products': "1, 2, 4, 10, 99"}
    response = client.post(f'/api/wallets/{wallet.id}/purchase', data=json.dumps(payload))
    assert response.status_code == 400
