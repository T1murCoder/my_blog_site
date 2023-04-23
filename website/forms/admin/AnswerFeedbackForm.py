from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Length


class AnswerFeedbackForm(FlaskForm):
    answer_feedback = TextAreaField("Answer to feedback:", validators=[Length(0, 140)])
    submit = SubmitField('Отправить')