from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Length


class FeedbackForm(FlaskForm):
    feedback = TextAreaField("Задайте вопрос или сообщите об ошибке:", validators=[Length(0, 140)])
    submit = SubmitField('Отправить')