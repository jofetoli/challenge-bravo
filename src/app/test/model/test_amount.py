import unittest

from aiohttp.web_exceptions import HTTPBadRequest
from model.amount import Amount

class AmountTests(unittest.TestCase):

    def test_correct_amount(self):
        amount = Amount('10.56')
        self.assertEqual(amount.value(), 10.56)

    def test_exponencial_amount(self):
        amount = Amount('2e56')
        self.assertEqual(amount.value(), 2e+56)

    def test_decimal_separator_amount(self):
        with self.assertRaises(HTTPBadRequest) as context:
            amount = Amount('10,56')

        self.assertEqual(context.exception.text, 'Amount (10,56) is an invalid positive decimal. Use ''.'' for decimal separator')

    def test_name_amount(self):
        with self.assertRaises(HTTPBadRequest) as context:
            amount = Amount('XPTO')

        self.assertEqual(context.exception.text, 'Amount (XPTO) is an invalid positive decimal. Use ''.'' for decimal separator')

    def test_none_amount(self):
        with self.assertRaises(HTTPBadRequest) as context:
            amount = Amount(None)

        self.assertEqual(context.exception.text, 'Amount (None) is an invalid positive decimal. Use ''.'' for decimal separator')

    def test_negative_amount(self):
        with self.assertRaises(HTTPBadRequest) as context:
            amount = Amount('-10.56')

        self.assertEqual(context.exception.text, 'Amount (-10.56) must be a positive decimal')
        
if __name__ == '__main__':
    unittest.main()
