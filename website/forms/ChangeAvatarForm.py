from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class ChangeAvatarForm(FlaskForm):
    avatar = FileField("Прикрепите изображение", validators=[DataRequired(), FileAllowed(['png', 'jpeg', 'jpg'], 'Неправильное расширение файла!')])
    submit = SubmitField('Изменить')