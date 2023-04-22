from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import Optional, Length, ValidationError
from flask_wtf.file import FileAllowed


def at_least_one_required():
    message = 'Вы не можете отправить пустой комментарий!'
    def _at_least_one_required(form, field):
        if not form.text.data and not form.files.data:
            raise ValidationError(message)
    return _at_least_one_required


class CommentForm(FlaskForm):
    text = TextAreaField('Введите комментарий:', validators=[at_least_one_required()])
    files = MultipleFileField("Прикрепите до 3-х изображений", validators=[Optional(),
                                                                           Length(max=3, message='Вы можете прикрепить максимум 3 файла!'),
                                                                           FileAllowed(['png', 'jpeg', 'jpg'], 'Неправильное расширение файла!'),
                                                                           at_least_one_required()])
    submit = SubmitField('Отправить')


