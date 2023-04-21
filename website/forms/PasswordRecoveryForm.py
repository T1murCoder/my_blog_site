from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, EmailField, TextAreaField
from wtforms.validators import DataRequired


class PasswordRecoveryForm(FlaskForm):
    email = EmailField('Введите почту, на которую зарегистрирован аккаунт', validators=[DataRequired()])
    submit = SubmitField('Отправить')