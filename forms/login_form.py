from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from data import db_session
from data.users import User


def validate_password(form, data):
    db_sess = db_session.create_session()
    val = db_sess.query(User).filter(User.login == form.login.data).first()
    db_sess.close()
    if not val or not val.check_password(form.password.data):
        raise ValidationError('Неверный логин или пароль')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), validate_password])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')