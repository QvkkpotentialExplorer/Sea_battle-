from flask import Flask
from data import db_session
from data.users import User
from flask_login import LoginManager
from blueprints.auth.auth_app import auth_pages

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'lJihdIUh12eIHUI34'

app.register_blueprint(auth_pages)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    db_sess.close()
    return user


if __name__ == '__main__':
    db_session.global_init("db/sea_battel.db")
    app.run()
