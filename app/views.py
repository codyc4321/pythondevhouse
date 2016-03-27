import os

from flask import render_template, request
from app import application

from .forms import MessageForm
from .email import Mailer

@application.route('/', methods=['GET', 'POST'])
def index(title='Learn Python where you live'):
    form = MessageForm()
    
    print(form.validate_on_submit())
    if request.method == "POST":
        if form.validate_on_submit():
            mailer = Mailer(os.environ.get('POSTMARK_KEY'))
            mailer._send(subject='yo', body=form.data['message'], 
                    html=None, sender='info@pythondevhouse.com', 
                    recipients=['cchilder@mail.usf.edu'], 
                    reply_to=form.data['email'], cc=None)
            return render_template('index.html', title=title, form=form, submission="valid")
        else:
            return render_template('index.html', title=title, form=form, submission="invalid")
    return render_template('index.html', title=title, form=form, submission="none")
                           
@application.route('/floorplan', methods=['GET'])
def floorplan():
    return render_template('floorplan.html',
                           title='Floorplan'
                           )
