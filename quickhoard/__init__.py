from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY='dev')

    app.config['MYSQL_DATABASE_USER'] = 'quickhoard'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'quickpassword'
    app.config['MYSQL_DATABASE_DB'] = 'qh'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'

    from . import auth, budget
    app.register_blueprint(auth.bp)
    app.register_blueprint(budget.bp)
    app.add_url_rule('/', endpoint='index')

    return app
