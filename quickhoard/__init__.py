from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY='dev')

    app.config['MYSQL_DATABASE_USER'] = 'quickhoard'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'quickpassword'
    app.config['MYSQL_DATABASE_DB'] = 'qh'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'

    if test_config is not None:
        app.config.from_mapping(test_config)

    from . import auth, budget, transaction
    app.register_blueprint(auth.bp)
    app.register_blueprint(budget.bp)
    app.register_blueprint(transaction.bp)
    app.add_url_rule('/', endpoint='index')

    return app
