import unittest
from unittest.mock import patch
from app import create_app

class ConverterTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_index_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'USD', response.data)

    @patch('app.get_exchange_rate')
    def test_conversion_success(self, mock_get_rate):
        mock_get_rate.return_value = 75.0
        response = self.client.post('/', data={
            'from_currency': 'USD',
            'to_currency': 'RUB',
            'amount': '10'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'750.0', response.data)

    def test_invalid_input(self):
        response = self.client.post('/', data={
            'from_currency': 'USD',
            'to_currency': 'RUB',
            'amount': 'not_a_number'
        })
        self.assertEqual(response.status_code, 200)
        # Проверяем русский текст через декодирование
        self.assertIn('числом', response.data.decode('utf-8'))

    @patch('app.get_exchange_rate')
    def test_api_failure(self, mock_get_rate):
        mock_get_rate.return_value = None
        response = self.client.post('/', data={
            'from_currency': 'USD',
            'to_currency': 'RUB',
            'amount': '10'
        })
        self.assertIn('Не удалось получить курс', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
