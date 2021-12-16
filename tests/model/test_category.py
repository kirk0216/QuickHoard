import unittest
from quickhoard.model.category import Category


class CategoryTest(unittest.TestCase):
    def test_isvalid_with_valid_category(self):
        category = Category(0, 'Test', '20.0')

        expected = (True, None)
        actual = category.is_valid()

        self.assertEqual(expected, actual, 'is_valid did not return the expected value.')

    def test_isvalid_with_invalid_category(self):
        category = Category()

        expected = (False, 'Please enter a name for your category.')
        actual = category.is_valid()

        self.assertEqual(expected, actual, 'is_valid did not return the expected value.')

    def test_parse(self):
        expected = {
            'id': 0,
            'name': 'Test',
            'goal': '20.0'
        }

        actual = Category()
        actual.parse(expected)

        self.assertEqual(expected['id'], actual.id, 'Category was not correctly parsed')
        self.assertEqual(expected['name'], actual.name, 'Category was not correctly parsed')
        self.assertEqual(expected['goal'], actual.goal, 'Category was not correctly parsed')


if __name__ == '__main__':
    unittest.main()
