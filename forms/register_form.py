from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from data import db_session
from data.users import User


def validate_login(form, data):
    db_sess = db_session.create_session()
    val = db_sess.query(User).filter(User.login == data.data).first()
    db_sess.close()
    if val:
        raise ValidationError('Логин уже существует')


class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), validate_login])
    password = PasswordField('Пароль', validators=[DataRequired(), EqualTo('confirm', message='Пароли не совпадают')])
    confirm = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Регистрация')