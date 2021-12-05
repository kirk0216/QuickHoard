from flask import Blueprint, render_template, session, redirect, url_for, request
from quickhoard.db import Database
from quickhoard.budget import Category
from datetime import date

bp = Blueprint('transaction', __name__, url_prefix='/transaction')


class Transaction:
    def __init__(self, date=None, recipient=None, category_id=None, amount=None, category=None):
        self.date = date
        self.recipient = recipient
        self.category_id = category_id
        self.category = category
        self.amount = amount

    def parse(self, row):
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


@bp.route('/')
def index():
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('auth.login'))

    database = Database()
    database.open()

    categories = get_categories(database, user_id)

    transactions = []

    sql = (
        'SELECT t.*, c.*, c.name as category FROM category c '
        'JOIN transaction t ON t.category_id = c.id '
        'WHERE c.user_id = %s AND MONTH(t.date) = %s '
        'ORDER BY date;'
    )

    cursor = database.query(sql, (user_id, date.today().month))

    for row in cursor:
        transaction = Transaction()
        transaction.parse(row)
        transactions.append(transaction)

    database.close()

    from calendar import month_name
    budget = {'year': date.today().year, 'month': month_name[date.today().month]}

    return render_template('transactions.html', budget=budget, categories=categories, transactions=transactions)


def get_categories(db, user_id):
    categories = []

    sql = (
        'SELECT * FROM category c '
        'LEFT JOIN transaction t ON t.category_id = c.id '
        'WHERE c.user_id = %s;'
    )

    cursor = db.query(sql, user_id)

    for row in cursor:
        category = Category()
        category.parse(row)
        categories.append(category)

    return categories

@bp.route('/add', methods=('GET', 'POST'))
def add_transaction():
    transaction = None

    if request.method == 'POST':
        transaction = Transaction(request.form['date'], request.form['recipient'], request.form['category_id'],
                                  request.form['amount'])

        database = Database()
        database.open()

        sql = (
            'INSERT INTO transaction '
            '(recipient, date, amount, category_id) '
            'VALUES (%s, %s, %s, %s);'
        )

        database.insert(sql, (transaction.recipient, transaction.date, transaction.amount, transaction.category_id))

        database.close()

    return redirect(url_for('transaction.index'))
