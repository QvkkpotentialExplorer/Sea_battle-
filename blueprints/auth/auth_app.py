from flask import Blueprint, render_template, redirect
from flask_login import login_user
from data.users import User
from data import db_session
from forms.login_form import LoginForm
from forms.register_form import RegisterForm


auth_pages = Blueprint('auth_page', __name__, template_folder='templates')


@auth_pages.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User(
            login=form.login.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return 'Вы зареганы'
    return render_template('register.html', form=form)


@auth_pages.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(1)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        db_sess.close()
        print(user.login)
        login_user(user, remember=form.remember_me.data)
        return f'Вы залогинены как {user.login}'
    return render_template('login.html', form=form)





