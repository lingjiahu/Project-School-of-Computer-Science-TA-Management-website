import os
import sys
sys.path.insert(0, '/home/xhu48/public_html/cgi-bin/venv/lib/python3.6/site-packages')

from flask import Flask, render_template, request
from db import init_app, get_db
from user import bp as user_bp

app = Flask(__name__, template_folder='templates')
app.register_blueprint(user_bp)
app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

init_app(app)

@app.route('/')
def home():
    if (request.method == 'GET'):
        return "hello"
    return render_template('hello.html')

@app.route('/register')
def register():
    connection = get_db()
    return "register"
        