from flaskr import app

@app.route('/')
def landding():
    return 'Landing Page'
