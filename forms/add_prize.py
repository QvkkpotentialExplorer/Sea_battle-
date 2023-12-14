from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired


class AddPrizeForm(FlaskForm):
    avatar = FileField(validators=[FileRequired(),
                                   FileAllowed(['jpg', 'png', 'jpeg'], 'Не тот файл')])
    name = StringField('Название приза', validators=[DataRequired()])
    description = StringField('Название приза', validators=[DataRequired()])
    submit = SubmitField('Добавить приз')