from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Length


class ChangeAboutForm(FlaskForm):
    about = TextAreaField("Расскажите о себе:", validators=[Length(0, 140)])
    submit = SubmitField('Изменить')