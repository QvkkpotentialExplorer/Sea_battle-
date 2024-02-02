from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, BooleanField, EmailField
from wtforms.validators import DataRequired, ValidationError
from flask import session


def code_validation(form, data):
    if form.validation_code.data != session.get('validation_key'):
        raise ValidationError('Не верный код')


class XMPPValidate(FlaskForm):
    validation_code = StringField('код подтверждения', validators=[DataRequired(), code_validation])
    submit = SubmitField('Войти')
