import unittest
from quickhoard.model.user import User


class UserTest(unittest.TestCase):
    def test_isvalid_with_valid_user(self):
        expected = (True, None)

        user = User('pat.kirk@test.com', 'Welcome24!')
        actual = user.is_valid()

        self.assertEqual(expected, actual, 'is_valid: Expected (True, None), got ' + str(actual))

    def test_isvalid_with_invalid_user(self):
        expected = (False, 'Email and password are required.')

        user = User()
        actual = user.is_valid()

        self.assertEqual(expected, actual, 'is_valid: Expected (True, None), got ' + str(actual))

    def test_parse(self):
        expected = {
            'id': 0,
            'email': 'patkirk@test.com',
            'password': 'Welcome24!',
            'failed_login': 3,
            'last_login': None
        }

        actual = User()
        actual.parse(expected)

        self.assertEqual(expected['id'], actual.id, 'Id was not parsed.')
        self.assertEqual(expected['email'], actual.email, 'Id was not parsed.')
        self.assertEqual(expected['password'], actual.password, 'Id was not parsed.')
        self.assertEqual(expected['failed_login'], actual.failed_login, 'Id was not parsed.')
        self.assertEqual(expected['last_login'], actual.last_login, 'Id was not parsed.')


if __name__ == '__main__':
    unittest.main()
