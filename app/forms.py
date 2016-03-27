from flask.ext.wtf import Form
from wtforms import StringField, TextField, TextAreaField
from wtforms.validators import DataRequired, Email


class MessageForm(Form):
    email = StringField('email', validators=[DataRequired("Please enter your email address"), Email("Please enter a valid email address")], render_kw={'placeholder': 'your email address'})
    message = TextAreaField('message', validators=[DataRequired("Please tell me about yourself and your goals")], render_kw={'placeholder': 'Have a question or want to check availability? Send me a message!'})

