from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange


class AddBoardForm(FlaskForm):
    n = IntegerField('Длина квадрата', validators=[NumberRange(1, 100)])
    submit = SubmitField('Добавить доску')