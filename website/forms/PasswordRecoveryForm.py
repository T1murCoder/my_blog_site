from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField
from wtforms.validators import DataRequired


class PasswordRecoveryForm(FlaskForm):
    email = EmailField('Введите почту, на которую зарегистрирован аккаунт', validators=[DataRequired()])
    submit = SubmitField('Отправить')