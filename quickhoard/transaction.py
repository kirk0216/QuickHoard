from flask import Blueprint, render_template, session, redirect, url_for, request
from quickhoard.db import Database
from quickhoard.budget import Category
from datetime import date
from quickhoard.model.transaction import Transaction

bp = Blueprint('transaction', __name__, url_prefix='/transaction')


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


@bp.route('/edit', methods=('GET', 'POST'))
def edit_transactions():
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('auth.login'))

    database = Database()
    database.open()

    categories = get_categories(database, user_id)

    if request.method == 'POST':
        transaction = Transaction()
        transaction.parse(request.form)

        sql = (
            'UPDATE transaction SET '
            'date = %s, recipient = %s, amount = %s, category_id = %s '
            'WHERE id = %s;'
        )

        database.execute(sql, (transaction.date, transaction.recipient, transaction.amount, transaction.category_id, transaction.id))
        database.commit()

        return redirect(url_for('transaction.index'))

    transactions = []

    sql = (
        'SELECT t.id AS transaction_id, t.*, c.*, c.name as category FROM category c '
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

    return render_template('transactions_edit.html', budget=budget, categories=categories, transactions=transactions)


@bp.route('/delete', methods=('POST',))
def delete():
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        database = Database()
        database.open()

        sql = (
            'DELETE FROM transaction '
            'WHERE id = %s;'
        )

        transaction_id = request.form['id']

        database.execute(sql, transaction_id)
        database.commit()

        database.close()

    return redirect(url_for('transaction.index'))
