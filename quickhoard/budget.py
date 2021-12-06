from flask import Blueprint, redirect, url_for, render_template, session, request, flash
from quickhoard.db import Database
from datetime import date

bp = Blueprint('budget', __name__)


class Budget:
    income = None
    expense = None
    categories = []

    def __init__(self, year, month):
        self.year = year

        from calendar import month_name
        self.month = month_name[month]

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


@bp.route('/')
def index():
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('auth.login'))

    database = Database()
    database.open()

    sql = (
        'SELECT c.id, c.name, cg.goal, '
        '	COALESCE(ABS(SUM(t.amount)), 0) AS spent, '
        '	COALESCE(cg.goal - ABS(SUM(t.amount)), cg.goal) AS remaining, '
        '	(SELECT COALESCE(ABS(SUM(amount)), 0) '
        '		FROM transaction '
        '        WHERE Amount < 0 '
        '			AND MONTH(date) = %(date)s '
        '			AND category_id in (SELECT id FROM category WHERE user_id = %(user_id)s) '
        '	) AS expense, '
        '	(SELECT COALESCE(ABS(SUM(amount)), 0) '
        '        FROM transaction '
        '        WHERE Amount > 0 '
        '			AND MONTH(date) = %(date)s '
        '			AND category_id in (SELECT id FROM category WHERE user_id = %(user_id)s) '
        '	) AS income '
        'FROM category c '
        'LEFT JOIN category_goal cg ON cg.category_id = c.id '
        'LEFT JOIN transaction t ON (t.category_Id = c.id AND MONTH(t.date) = cg.month) '
        'WHERE c.user_id = %(user_id)s AND cg.month = %(date)s '
        'GROUP BY c.id;'
    )

    cursor = database.query(sql, {"user_id": user_id, "date": date.today().month })

    budget = Budget(date.today().year, date.today().month)
    budget.parse(cursor.fetchall())

    database.close()

    return render_template('dashboard.html', budget=budget)


@bp.route('/category/add', methods=('GET', 'POST'))
def add_category():
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        category = Category(None, request.form['name'], request.form['amount'])

        valid, error = category.is_valid()

        if valid:
            database = Database()
            database.open()

            sql = 'INSERT INTO category (name, user_id) VALUES (%s, %s);'
            category_id = database.insert(sql, (category.name, user_id))

            sql = 'INSERT INTO category_goal (goal, year, month, category_id) VALUES (%s, YEAR(CURDATE()), MONTH(CURDATE()), %s);'
            database.insert(sql, (category.goal, category_id))

            database.close()

            flash(f'Category {category.name} added!', 'alert-success')

    if error is not None:
        flash(error, 'alert-danger')

    return redirect(url_for('index'))


@bp.route('/category/edit', methods=('GET', 'POST'))
def edit_categories():
    user_id = session.get('user_id')

    database = Database()
    database.open()

    if request.method == 'POST':
        category_id = request.form['category_id'] if 'category_id' in request.form else None
        name = request.form['name'] if 'name' in request.form else None
        goal_id = request.form['goal_id'] if 'goal_id' in request.form else None
        goal = request.form['goal'] if 'goal' in request.form else None

        error = None

        if category_id is None or name is None or goal_id is None or goal is None:
            error = 'Missing values.'
        elif len(name) == 0:
            error = 'Name cannot be blank.'
        elif len(goal) == 0:
            error = 'Amount cannot be blank.'

        if error is None:
            sql = (
                'UPDATE category SET name = %s WHERE id = %s;'
            )

            database.execute(sql, (name, category_id))

            sql = (
                'UPDATE category_goal SET goal = %s WHERE id = %s;'
            )

            database.execute(sql, (goal, goal_id))
            database.commit()

            flash('Saved changes.', 'alert-success')
        else:
            flash(error, 'alert-danger')


    sql = (
        'SELECT c.id, c.name, cg.id AS goal_id, cg.goal FROM category c '
        'LEFT JOIN category_goal cg ON (cg.category_id = c.id AND cg.year = YEAR(CURDATE()) AND cg.month = MONTH(CURDATE())) '
        'WHERE c.user_id = %s;'
    )

    cursor = database.query(sql, user_id)
    categories = []

    for row in cursor:
        category = Category()
        category.parse(row)
        categories.append(category)

    database.close()

    from calendar import month_name
    budget = {'year': date.today().year, 'month': month_name[date.today().month]}

    return render_template('category.html', budget=budget, categories=categories)


@bp.route('/category/delete', methods=['POST'])
def delete_category():
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('auth.login'))

    database = Database()
    database.open()

    sql = "DELETE FROM category WHERE id = %s;"
    category_id = request.form['category_id']

    database.execute(sql, category_id)
    database.commit()

    database.close()

    flash(f'Deleted category.', 'alert-info')

    return redirect(url_for('budget.edit_categories'))
