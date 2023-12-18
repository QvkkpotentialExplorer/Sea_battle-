from data import db_session
db_session.global_init('./db/sea_battel.db')

from flask import Flask
from data.db_session import db_sess
from data.users import User
from flask_login import LoginManager
from blueprints.auth.auth_app import auth_pages
from blueprints.main_page.main_page import main_page
from blueprints.admin.admin import admin
from blueprints.boards.board import board
from blueprints.api.api import api

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'lJihdIUh12eIHUI34'

app.register_blueprint(auth_pages)
app.register_blueprint(main_page)
app.register_blueprint(admin)
app.register_blueprint(board)
app.register_blueprint(api)


@login_manager.user_loader
def load_user(user_id):
    user = db_sess.query(User).get(user_id)
    return user


if __name__ == '__main__':
    app.run()
