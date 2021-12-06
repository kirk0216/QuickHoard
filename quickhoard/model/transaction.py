class Transaction:
    def __init__(self, date=None, recipient=None, category_id=None, amount=None, category=None):
        self.id = None
        self.date = date
        self.recipient = recipient
        self.category_id = category_id
        self.category = category
        self.amount = amount

    def parse(self, row):
        if 'id' in row:
            self.id = row['id']

        if 'date' in row:
            self.date = row['date']

        if 'recipient' in row:
            self.recipient = row['recipient']

        if 'category_id' in row:
            self.category_id = row['category_id']

        if 'category' in row:
            self.category = row['category']

        if 'amount' in row:
            self.amount = row['amount']