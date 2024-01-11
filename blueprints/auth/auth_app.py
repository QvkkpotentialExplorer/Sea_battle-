from flask import Blueprint, render_template, redirect, url_for, session, abort
from flask_login import login_user, logout_user
from data.users import User
from forms.xmpp_validate import XMPPValidate
from data.db_session import db_sess
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
import random
from string import ascii_letters
import requests

auth_pages = Blueprint('auth_page', __name__, template_folder='../templates', static_folder='static', url_prefix='/auth/')


@auth_pages.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session['login'] = form.login.data
        session['password'] = form.password.data
        session['jid'] = form.jid.data
        return redirect(url_for('auth_page.send_key'))
    return render_template('register.html', form=form)


@auth_pages.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        login_user(user, remember=form.remember_me.data)
        return redirect(location=url_for('profile.user'))

    return render_template('login.html', form=form)


@auth_pages.route('/xmpp_validate', methods=['GET', 'POST'])
def xmpp_validate():
    form = XMPPValidate()
    if form.validate_on_submit():
        if session['validation_key'] != form.validation_code.data:
            return 'не верный код'
        user = User(
            login=session.get('login'),
            jid=session.get('jid'),
            is_admin=False
        )
        user.set_password(session.get('password'))
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('validate.html', form=form)


@auth_pages.route('/send_key')
def send_key():
    session['validation_key'] = ''.join([random.choice(ascii_letters) for _ in range(8)])
    if session.get('jid') is None:
        return abort(404)
    url = "http://nekopara.ru:5443/api/send_message"
    data = {
        "type": "headline",
        "from": "chokolla@nekopara.ru",
        "to": f"{session.get('jid')}",
        "subject": "Restart",
        "body": f"Ваш код авторизации: {session.get('validation_key')}"
    }

    res = requests.post(url, json=data, auth=("api@nekopara.ru", "wTr7Rw_QUSeV_SAR"))
    return redirect(url_for('auth_page.xmpp_validate'))


@auth_pages.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/')
