import pytest
from app import app, get_exchange_rate
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_negative_amount(client):
    response = client.post('/', data={'amount': '-100', 'from_currency': 'USD', 'to_currency': 'RUB'})
    assert b'положительной' in response.data

def test_zero_amount(client):
    response = client.post('/', data={'amount': '0', 'from_currency': 'USD', 'to_currency': 'RUB'})
    assert b'положительной' in response.data

def test_non_numeric_amount(client):
    response = client.post('/', data={'amount': 'abc', 'from_currency': 'USD', 'to_currency': 'RUB'})
    assert b'числом' in response.data

def test_empty_amount(client):
    response = client.post('/', data={'amount': '', 'from_currency': 'USD', 'to_currency': 'RUB'})
    assert b'положительной' in response.data

@patch('app.requests.get')
def test_get_exchange_rate_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {'rates': {'RUB': 90.5}}
    rate = get_exchange_rate('USD', 'RUB')
    assert rate == 90.5

@patch('app.requests.get')
def test_get_exchange_rate_failure(mock_get):
    mock_get.side_effect = Exception('API error')
    rate = get_exchange_rate('USD', 'RUB')
    assert rate is None

def test_get_exchange_rate_same_currency():
    rate = get_exchange_rate('USD', 'USD')
    assert rate == 1.0

@patch('app.get_exchange_rate')
def test_conversion_success(mock_rate, client):
    mock_rate.return_value = 90.5
    response = client.post('/', data={'amount': '10', 'from_currency': 'USD', 'to_currency': 'RUB'})
    assert b'905.0' in response.data