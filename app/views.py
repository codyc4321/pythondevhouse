import os

from flask import render_template, request
from app import application

from .forms import MessageForm
from .email import Mailer


guided_learning ="""Studying web development is hard when you're alone.  \
Enjoy the journey with a mentor that'll remove much of the uncertainty and confusion that comes from learning in isolation."""

no_frustration = """Getting stuck usually means posting to a forum and waiting days or weeks for a response. \
Remove these roadblocks and accelerate your learning by living in a house full of programmers, with an instructor/mentor."""

new_career = """Take the guess work out of your path to that entry level job and move forward with the confidence that all \
your efforts are contributing to your development and employability."""

my_story_1 = """I'm a backend python/django engineer for a well established mutual fund and part-time backend python/flask engineer \
for an early startup here in Austin, TX.  I build daily in Python, Django, and Flask, and occasionally I use Javascript and JQuery. \
I specialize in metaprogramming (writing programs to write my programs for me), unittesting (essential to good software), and developing/fixing APIs. 
But just 2 years ago I was a struggling chemist in a dying job market."""
                            
my_story_2 = """I began learning python online through udacity and with the training of my friend who has a C.S. degree, \
and my friend who was learning web development. I decided to change my future and become a developer full-time."""

my_story_3 = """After just 3 weeks of individual study and one-on-one training from my best friend I wrote a \
calendar calculator in python, and went from aspirant to junior developer. This was all I needed to launch a successful \
career and leave my stress behind, and I can attest to how beneficial one-on-one guidance can be. Now, I'd like to launch YOUR career!"""


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
    return render_template('index.html', title=title, form=form, submission="none",
                           guided_learning=guided_learning, no_frustration=no_frustration, new_career=new_career,
                           my_story_1=my_story_1, my_story_2=my_story_2, my_story_3=my_story_3)


@application.route('/floorplan', methods=['GET'])
def floorplan():
    return render_template('floorplan.html', title='Floorplan')
