from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, EmailField, TextAreaField, FileField
from wtforms.validators import DataRequired


class ChangeAvatarForm(FlaskForm):
    avatar = FileField("Прикрепите изображение", validators=[DataRequired()])
    submit = SubmitField('Изменить')