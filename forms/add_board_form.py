from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange


class AddBoardForm(FlaskForm):
    n = IntegerField('Длина квадрата', validators=[NumberRange(1, 100)])
    default_shoots = IntegerField('Длина квадрата', validators=[NumberRange(1, 10000)])
    submit = SubmitField('Добавить доску')