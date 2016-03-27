from flask import render_template, request
from app import app

from .forms import MessageForm
from .email import Mailer

@app.route('/', methods=['GET', 'POST'])
def index(title='Learn Python where you live'):
    form = MessageForm()
    
    print(form.validate_on_submit())
    if request.method == "POST":
        if form.validate_on_submit():
            mailer = Mailer("ba7663a2-19ba-4a42-bf69-5b4485fcab6f")
            mailer._send(subject='yo', body=form.data['message'], 
                    html=None, sender='info@pythondevhouse.com', 
                    recipients=['cchilder@mail.usf.edu'], 
                    reply_to=form.data['email'], cc=None)
            return render_template('index.html', title=title, form=form, submission="valid")
        else:
            return render_template('index.html', title=title, form=form, submission="invalid")
    return render_template('index.html', title=title, form=form, submission="none")
                           
@app.route('/floorplan', methods=['GET'])
def floorplan():
    return render_template('floorplan.html',
                           title='Floorplan'
                           )