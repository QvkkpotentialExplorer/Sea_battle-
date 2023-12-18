from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from data.db_session import db_sess
from data.users import User


def validate_password(form, data):
    val = db_sess.query(User).filter(User.login == form.login.data).first()
    if not val :
        raise ValidationError('Такого логина нет')
    elif not val.check_password(form.password.data):
        raise ValidationError('Неверный пароль')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), validate_password])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')