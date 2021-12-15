from quickhoard.model.category import Category


# Contains information about a budget
class Budget:
    income = None
    expense = None
    categories = []

    def __init__(self, year, month):
        self.year = year

        from calendar import month_name
        self.month = month_name[month]

    # Parses a budget from a dictionary object.
    def parse(self, result):
        if result is None:
            return

        self.categories.clear()

        for row in result:
            if self.income is None and 'income' in row:
                self.income = row['income']

            if self.expense is None and 'expense' in row:
                self.expense = row['expense']

            category = Category()
            category.parse(row)

            self.categories.append(category)
