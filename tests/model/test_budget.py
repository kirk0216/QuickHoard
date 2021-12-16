import unittest
from quickhoard.model.budget import Budget


class BudgetTest(unittest.TestCase):
    def test_parse(self):
        expected = [
            {
                'year': 2020,
                'month': 'October',
                'income': '20.0',
                'expense': '25.0',
                'id': 0,
                'name': 'Test',
                'goal': '33.0'
            }
        ]

        actual = Budget(2020, 10)
        actual.parse(expected)

        self.assertEqual(expected[0]['year'], actual.year, 'Budget was not correctly parsed')
        self.assertEqual(expected[0]['month'], actual.month, 'Budget was not correctly parsed')
        self.assertEqual(expected[0]['income'], actual.income, 'Budget was not correctly parsed')
        self.assertEqual(expected[0]['expense'], actual.expense, 'Budget was not correctly parsed')


if __name__ == '__main__':
    unittest.main()
