from flask.ext.wtf import Form
from wtforms import StringField, TextField
from wtforms.validators import DataRequired


class MessageForm(Form):
    email = StringField('email', validators=[DataRequired()], render_kw={'placeholder': 'your email address'})
    message = TextField('message', validators=[DataRequired()], render_kw={'placeholder': 'Have a question or want to check availability? Send me a message!'})

