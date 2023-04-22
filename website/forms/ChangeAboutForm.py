from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length


class ChangeAboutForm(FlaskForm):
    about = TextAreaField("Расскажите о себе:", validators=[Length(0, 140)])
    submit = SubmitField('Изменить')