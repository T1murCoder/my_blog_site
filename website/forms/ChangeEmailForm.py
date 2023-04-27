from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField
from wtforms.validators import DataRequired


class ChangeEmailForm(FlaskForm):
    email = EmailField("Введите имя:", validators=[DataRequired()])
    submit = SubmitField('Изменить')