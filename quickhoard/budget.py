from flask import Blueprint, redirect, url_for, render_template, session, request, flash
from quickhoard.db import Database

bp = Blueprint('budget', __name__)


@bp.route('/')
def index():
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('auth.login'))

    database = Database()
    database.open()

    sql = (
        'SELECT b.Id as Budget_Id, b.User_Id, b.Name, c.Name AS Category, c.Goal, '
        '	COALESCE(ABS(SUM(t.Amount)), 0) AS Spent, '
        '    COALESCE(c.Goal - ABS(SUM(t.Amount)), c.Goal) AS Remaining, '
        '	(SELECT COALESCE(ABS(SUM(Amount)), 0) FROM `transaction` WHERE Amount < 0) AS Expense, '
        '    (SELECT COALESCE(ABS(SUM(Amount)), 0) FROM `transaction` WHERE Amount > 0) AS Income '
        'FROM budget b '
        'LEFT JOIN category c ON c.Budget_Id = b.Id '
        'LEFT JOIN `transaction` t ON t.Category_Id = c.Id '
        'WHERE b.User_Id = %s '
        'GROUP BY c.Id;'
    )

    cursor = database.query(sql, user_id)
    budget = cursor.fetchall()

    database.close()

    return render_template('dashboard.html', budget=budget)


@bp.route('/category/add', methods=('GET', 'POST'))
def add_category():
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form['name'] or None
        amount = request.form['amount'] or None
        budget_id = request.form['budget_id'] or None

        error = None

        if name is None or budget_id is None:
            error = 'An error was encountered. Please try again.'
        else:
            if amount is None:
                amount = '0.00'

            database = Database()
            database.open()

            sql = 'INSERT INTO category (Name, Goal, Budget_Id) VALUES (%s, %s, %s);'
            database.execute(sql, (name, amount, budget_id))
            database.commit()

            database.close()

            flash(f'Category {name} added!', 'alert-success')

    if error is not None:
        flash(error, 'alert-danger')

    return redirect(url_for('index'))
