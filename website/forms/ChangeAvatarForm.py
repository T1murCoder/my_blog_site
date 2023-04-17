from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, EmailField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class ChangeAvatarForm(FlaskForm):
    avatar = FileField("Прикрепите изображение", validators=[DataRequired(), FileAllowed(['jpg', 'png'], 'Неправильное расширение файла!')])
    submit = SubmitField('Изменить')