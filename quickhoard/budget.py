from flask import Blueprint, redirect, url_for, render_template, session, request, flash
from quickhoard.db import Database
from datetime import date

bp = Blueprint('budget', __name__)


@bp.route('/')
def index():
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('auth.login'))

    database = Database()
    database.open()

    sql = (
        'SELECT c.name, cg.goal, '
        '	COALESCE(ABS(SUM(t.amount)), 0) AS spent, '
        '   COALESCE(cg.goal - ABS(SUM(t.amount)), cg.goal) AS remaining, '
        '	(SELECT COALESCE(ABS(SUM(amount)), 0) FROM `transaction` WHERE Amount < 0) AS expense, '
        '   (SELECT COALESCE(ABS(SUM(amount)), 0) FROM `transaction` WHERE Amount > 0) AS income '
        'FROM category c '
        'LEFT JOIN category_goal cg ON cg.category_id = c.id '
        'LEFT JOIN `transaction` t ON (t.category_Id = c.id AND MONTH(t.date) = cg.month) '
        'WHERE c.user_id = %s '
        'GROUP BY c.id;'
    )

    cursor = database.query(sql, user_id)
    budget = cursor.fetchall()

    database.close()

    current_date = date.today()

    return render_template('dashboard.html', budget=budget, budget_month=current_date.strftime('%B %Y'))


@bp.route('/category/add', methods=('GET', 'POST'))
def add_category():
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form['name'] or None
        amount = request.form['amount'] or None

        error = None

        if name is None:
            error = 'Please enter a name for your category.'
        else:
            if amount is None:
                amount = '0.00'

            database = Database()
            database.open()

            sql = 'INSERT INTO category (name, user_id) VALUES (%s, %s);'
            category_id = database.insert(sql, (name, user_id))

            sql = 'INSERT INTO category_goal (goal, year, month, category_id) VALUES (%s, YEAR(CURDATE()), MONTH(CURDATE()), %s);'
            database.insert(sql, (amount, category_id))

            database.close()

            flash(f'Category {name} added!', 'alert-success')

    if error is not None:
        flash(error, 'alert-danger')

    return redirect(url_for('index'))
