import os
import sys
sys.path.insert(0, '/home/xhu48/public_html/cgi-bin/venv/lib/python3.6/site-packages')

from flask import Flask, render_template, request, flash, g, url_for, redirect, session
from db import init_app, get_db
import user, rateTA, admin

app = Flask(__name__, template_folder='templates')
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

app.config['UPLOAD_FOLDER'] = 'static/files'

app.add_url_rule('/hello', view_func=user.hello)
app.add_url_rule('/landing', view_func=user.landing)
app.add_url_rule('/register', view_func=user.register)
app.add_url_rule('/logout', view_func=user.logout)
app.add_url_rule('/dashboard', view_func=user.dashboard)
app.add_url_rule('/selectCourse', view_func=rateTA.selectCourse)

app.add_url_rule('/info', view_func=admin.info)
app.add_url_rule('/courseinfo', view_func=admin.courseinfo)
app.add_url_rule('/update', view_func=admin.update)
app.add_url_rule('/adminimport', view_func=admin.adminimport)
#app.add_url_rule('/rate', view_func=rateTA.rate)

init_app(app)
class User:
    def __init__(self, userid, firstname, lastname, studentId, username, isStudent, isProf, isSysop, isAdmin, isTA):
        self.userid = userid
        self.firstname = firstname
        self.lastname = lastname
        self.studentId = studentId
        self.username = username
        self.isStudent = isStudent 
        self.isProf = isProf
        self.isSysop = isSysop 
        self.isAdmin = isAdmin 
        self.isTA = isTA

@app.before_request
def before_request():
    g.user = None
 
    if 'user_id' in session:
        connection = get_db()
        query = "SELECT * FROM users WHERE userid='{}'".format(session['user_id'])
        cursor = connection.execute(query)
        result = cursor.fetchall()
        cursor.close()
        query2 = "SELECT * FROM userAccounts WHERE username='{}'".format(result[0][4])
        cursor2 = connection.execute(query2)
        result2 = cursor2.fetchall()
        cursor2.close()
        user = User(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result2[0][3]==1, result2[0][4]==1, result2[0][5]==1, result2[0][6]==1, result2[0][7]==1)
        g.user = user

'''
@app.route("/register", methods=["GET", "POST"])
def register():
    color = "red"
    currentTerm = "Winter 2022"
    connection = get_db()
    cursor = connection.execute('SELECT coursenum, coursename FROM courses')
    courselist = cursor.fetchall()
    cursor.close()

    if request.method == 'POST':
        # get the parameter from the form
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        sid = request.form.get('studentid')
        uname = request.form.get('username')
        password = request.form.get('password')
        cpassword = request.form.get('confirmpassword')
        email = request.form.get('email')
        course = request.form.getlist('course')
        
        # get database connection
        connection = get_db()
        
        # validate username
        query = "SELECT * FROM users WHERE username='{}'".format(uname)
        cursor = connection.execute(query)
        result = cursor.fetchall()
        cursor.close()
        uname_exist = bool(result)

            
        # validate email
        query = "SELECT * FROM userAccounts WHERE useremail='{}'".format(email)
        cursor = connection.execute(query)
        result = cursor.fetchall()
        cursor.close()
        email_exist = bool(result)
        
        if uname_exist:
            flash('The username already exists. Try again.')
        elif email_exist:
            flash('The email is already registered. Try again.')
        else:
            # sql
            query1 = "INSERT INTO userAccounts (userpassword, username, useremail, isStudent, isProf, isSysop, isAdmin, isTA) VALUES ('{}', '{}', '{}', 1, 0, 0, 0, 0)".format(password, uname, email)
            query2 = "INSERT INTO users (firstname, lastname, studentId, username) VALUES ('{}', '{}', {}, '{}')".format(fname, lname, sid, uname)
            
            # get cursor
            cur1 = connection.execute(query1)
            cur2 = connection.execute(query2)
            curs = []
            for c in course:
                query3 = "INSERT INTO registeredTable (studentId, courseNum, term) VALUES ({}, '{}', '{}')".format(sid, c, currentTerm)
                cur = connection.execute(query3)
                curs.append(cur)
            
            connection.commit()
            # close
            cur1.close()
            cur2.close()
            for cur in curs:
                cur.close()
            connection.close()
            color = 'green'
            flash('You have registered successfully.')
    return render_template("register.html", courselist=courselist, color=color)

#  login should redirect back to landing with login disappear and welcome instead


@app.route("/landing", methods=["GET", "POST"])
def landing():
    if not g.user:
        visible = "display: show"
    else:
        visible = "display: none"

    if request.method == 'POST':
        session.pop('user_id', None)
        uname = request.form.get('username', None)
        password = request.form.get('password', None)

        # get database connection
        connection = get_db()
        
        # validate username
        query = "SELECT * FROM userAccounts WHERE username='{}' AND userpassword='{}'".format(uname, password)
        cursor = connection.execute(query)
        result = cursor.fetchall()
        cursor.close()
        user_exist = bool(result)
        if user_exist:
            query = "SELECT * FROM users WHERE username='{}'".format(uname)
            cursor = connection.execute(query)
            result = cursor.fetchall()
            cursor.close()
            user_id = result[0][0]
            session['user_id'] = user_id
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect username or password. Try again.')

    return render_template("landing.html", visible=visible)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop('user_id')
    return redirect(url_for('landing'))

# profile should be replaced with the dashboard
@app.route("/dashboard")
def dashboard():
    admin = "display: none"
    manage = "display: none"
    rating = "display: none"
    sysop = "display: none"
    if not g.user:
        return redirect(url_for('landing'))
    else:
        if g.user.isAdmin:
            admin = "display: show"
            manage = "display: show"
            sysop = "display: show"
        if g.user.isStudent:
            rating = "display: show"
        if g.user.isProf:
            manage = "display: show"
            rating = "display: show"
        if g.user.isSysop:
            admin = "display: show"
            manage = "display: show"
            rating = "display: show"
            sysop = "display: show"
        if g.user.isTA:
            manage = "display: show"
            rating = "display: show"
        return render_template("dashboard.html", admin=admin, manage=manage, rating=rating, sysop=sysop)

'''


        