from flask import Blueprint, redirect, url_for, render_template, session
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
        'SELECT b.Id, b.User_Id, b.Name, c.Name AS Category, c.Goal, '
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
    print(budget)

    database.close()

    return render_template('dashboard.html', budget=budget)
