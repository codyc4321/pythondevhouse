from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    print(app.root_path)
    return render_template('index.html',
                           title='Learn Python where you live',
                           )