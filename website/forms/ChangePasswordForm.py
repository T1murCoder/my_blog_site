from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ChangePasswordForm(FlaskForm):
    old_password = StringField("Введите старый пароль", validators=[DataRequired()])
    new_password = StringField("Введите новый пароль", validators=[DataRequired()])
    repeat_new_password = StringField("Повторите новый пароль", validators=[DataRequired()])
    submit = SubmitField('Изменить')