from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField, HiddenField
from wtforms.validators import NumberRange, DataRequired, ValidationError
from data.prizes import Prize
from data.ships import Ship
from data.boards import Board
from data.db_session import db_sess


def coords_validator(form, field):
    ships = db_sess.query(Ship).filter(Ship.x == form.x.data, Ship.y == form.y.data,
                                       Ship.board_id == form.board_id.data).first()
    if ships is None:
        raise ValidationError('На этих координатах не было корабля')


class DeleteShipForm(FlaskForm):
    board_id = HiddenField()
    x = IntegerField('x', validators=[NumberRange(min=0)])
    y = IntegerField('y', validators=[NumberRange(min=0)])
    submit = SubmitField('Удалить', validators=[coords_validator])