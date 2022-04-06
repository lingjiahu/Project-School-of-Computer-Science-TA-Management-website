import os
import subprocess as sp
from flask import Flask, render_template, request, url_for, flash, Markup

app = Flask(__name__)
from flaskr.endpoint import *

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # upload floder
    app.config['UPLOAD_FOLDER'] = 'static/files'
    
    from . import db
    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
        
if __name__ == "__main__":
    app.run(debug=True)
