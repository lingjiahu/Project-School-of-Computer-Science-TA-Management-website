import os
from flask import Flask
from flaskr.sysop import bp as sys_bp

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(sys_bp)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # upload floder
    app.config['UPLOAD_FOLDER'] = 'static/files'
    

    from . import db
    db.init_app(app)

    def query_db(query,args=(),one=False):
        cur = db.get_db().execute(query,args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

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


# if __name__ == "__main__":
#     app.run(debug=True)
