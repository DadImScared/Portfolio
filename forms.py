from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email


class ContactForm(Form):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    message = TextAreaField('Message', validators=[DataRequired()])
