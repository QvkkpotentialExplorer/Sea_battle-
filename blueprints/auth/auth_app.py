from flask import Blueprint, render_template, redirect, url_for, session, abort
from flask_login import login_user, logout_user, current_user
from data.users import User
from data.db_session import db_sess
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
import random
from string import ascii_letters
import requests
from crypto.gen_url import gen_url

auth_pages = Blueprint('auth_page', __name__, template_folder='../templates', static_folder='static', url_prefix='/auth/')


@auth_pages.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            login=form.login.data,
            is_admin=False
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect(url_for('auth_page.login'))
    return render_template('register.html', form=form)


@auth_pages.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        print(user)
        login_user(user, remember=form.remember_me.data)
        print(gen_url(current_user.id, 1))
        return redirect(location=url_for('profile.user'))

    return render_template('login.html', form=form)


@auth_pages.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/')
