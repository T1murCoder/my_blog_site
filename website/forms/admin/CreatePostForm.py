from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, EmailField, TextAreaField, URLField
from wtforms.validators import DataRequired


class CreatePostForm(FlaskForm):
    post_url = URLField('Ссылка на пост', validators=[DataRequired()])
    submit = SubmitField('Создать')