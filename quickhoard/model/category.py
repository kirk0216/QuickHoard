class Category:
    def __init__(self, id=None, name=None, goal=None):
        self.id = id
        self.name = name or None
        self.goal_id = None
        self.goal = goal or '0.00'
        self.spent = None
        self.remaining = None

    def is_valid(self):
        error = None

        if self.name is None:
            error = 'Please enter a name for your category.'
        elif not self.goal.isnumeric():
            error = 'Category goal must be a number.'
        elif float(self.goal) < 0:
            error = 'Category goal must be a positive number.'

        return error is None, error

    def parse(self, result):
        if result is None:
            return

        if 'id' in result:
            self.id = result['id']

        if 'name' in result:
            self.name = result['name']

        if 'goal' in result:
            self.goal = result['goal']

        if 'goal_id' in result:
            self.goal_id = result['goal_id']

        if 'spent' in result:
            self.spent = result['spent']

        if 'remaining' in result:
            self.remaining = result['remaining']