from flask import render_template
from app import app

from .forms import MessageForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MessageForm()
    return render_template('index.html',
                           title='Learn Python where you live',
                           form=form
                           )
                           
@app.route('/floorplan', methods=['GET'])
def floorplan():
    return render_template('floorplan.html',
                           title='Floorplan'
                           )