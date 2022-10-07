from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = 'database.db'


def initiate():
    app.config['SECRET_KEY'] = 'h4sski'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.run(debug=True)
    db.init_app(app)


def create_db(app):
    if not path.exists('/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


def main():
    initiate()

    from views import views
    from auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from models import User, Activity
    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


# if __name__ == '__main__':
main()
