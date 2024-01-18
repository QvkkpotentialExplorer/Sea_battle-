from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired
from wtforms.validators import Length
from data.db_session import db_sess


class AddPrizeForm(FlaskForm):
    avatar = FileField(validators=[FileRequired(),
                                   FileAllowed(['jpg', 'png', 'jpeg'], 'Не тот файл')])
    name = StringField('Название приза', validators=[DataRequired(),Length(min=5,max=20,message="Название должно быть не больше 20 символов")])
    description = StringField('Описание', validators=[DataRequired()])
    submit = SubmitField('Добавить приз')