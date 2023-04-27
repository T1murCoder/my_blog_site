from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class ChangeNameForm(FlaskForm):
    name = StringField("Введите имя:", validators=[DataRequired()])
    submit = SubmitField('Изменить')