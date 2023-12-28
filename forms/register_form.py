from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, EmailField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from data.users import User
from data.db_session import db_sess


def validate_login(form, data):
    val = db_sess.query(User).filter(User.login == data.data).first()
    if val:
        raise ValidationError('Этот логин уже занят , придумайте другой')


class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), validate_login])
    password = PasswordField('Пароль', validators=[DataRequired(), EqualTo('confirm', message='Пароли не совпадают')])
    confirm = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    jid = EmailField('xmpp адрес')
    submit = SubmitField('Регистрация')
