import re

class User:
    def __init__(self, email=None, password=None):
        self.id = None
        self.email = email
        self.password = password
        self.failed_login = 0
        self.last_login = None

    def parse(self, result):
        if result is None:
            return

        self.id = result['id']
        self.email = result['email']
        self.password = result['password']
        self.failed_login = result['failed_login']
        self.last_login = result['last_login']

    def is_valid(self):
        error = None

        if not self.email or not self.password:
            error = 'Email and password are required.'
        elif len(self.password) < 8:
            error = 'Password must be at least 8 characters long.'

        has_letter = re.search(r'\w', self.password) is not None
        has_number = re.search(r'\d', self.password) is not None
        has_special = re.search(r'\W', self.password) is not None

        if not has_letter or not has_number or not has_special:
            error = 'Password is not complex enough. Please include at least 1 letter, 1 number, ' \
                    'and 1 special character (!, @, #, or $).'

        return error is None, error
