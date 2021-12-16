import unittest
from quickhoard.model.transaction import Transaction


class CategoryTest(unittest.TestCase):
    def test_parse(self):
        expected = {
            'id': 0,
            'date': '2021-12-01',
            'recipient': '20.0',
            'amount': '20.0',
            'category_id': 1,
        }

        actual = Transaction()
        actual.parse(expected)

        self.assertEqual(expected['id'], actual.id, 'Id was not correctly parsed')
        self.assertEqual(expected['date'], actual.date, 'Date was not correctly parsed')
        self.assertEqual(expected['recipient'], actual.recipient, 'Recipient was not correctly parsed')
        self.assertEqual(expected['amount'], actual.amount, 'Amount was not correctly parsed')
        self.assertEqual(expected['category_id'], actual.category_id, 'Category_Id was not correctly parsed')


if __name__ == '__main__':
    unittest.main()
