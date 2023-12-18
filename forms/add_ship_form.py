from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.validators import NumberRange, DataRequired
from data.db_session import db_sess


class AddShipForm(FlaskForm):
    x = IntegerField('x', validators=[NumberRange(min=0), DataRequired()])
    y = IntegerField('y', validators=[NumberRange(min=0), DataRequired()])
    prize = SelectField('prizes', validators=[DataRequired()])
    submit = SubmitField('Добавить корабль')