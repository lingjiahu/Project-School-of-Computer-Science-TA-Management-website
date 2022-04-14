from dataclasses import dataclass
from flask import Blueprint, render_template, request, flash, g, url_for, redirect, session
import db

bp = Blueprint("user", __name__, url_prefix="/user")

@dataclass
class User:
    userid: int
    firstname: str
    lastname: str
    studentId: int
    username: str

@bp.before_request
def before_request():
    g.user = None
 
    if 'user_id' in session:
        connection = db.get_db()
        query = "SELECT * FROM users WHERE userid='{}'".format(session['user_id'])
        cursor = connection.execute(query)
        result = cursor.fetchall()
        cursor.close()
        user = User(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
        g.user = user
    else :
        pass
    
    
@bp.route("/register2", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        # get the parameter from the form
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        sid = request.form.get('studentid')
        uname = request.form.get('username')
        password = request.form.get('password')
        cpassword = request.form.get('confirmpassword')
        email = request.form.get('email')
        
        # get database connection
        connection = db.get_db()

        # sql
        query1 = "INSERT INTO userAccounts (userpassword, username, useremail, isStudent, isProf, isSysop, isAdmin, isTA) VALUES ('{}', '{}', '{}', 1, 0, 0, 0, 0)".format(password, uname, email)
        query2 = "INSERT INTO users (firstname, lastname, studentId, username) VALUES ('{}', '{}', {}, '{}')".format(fname, lname, sid, uname)
        
        # get cursor
        cur1 = connection.execute(query1)
        cur2 = connection.execute(query2)
        connection.commit()
        # close
        cur1.close()
        cur2.close()
        
    return render_template("register.html")

@bp.route("/register", methods=["GET", "POST"])
def register2():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        # get the parameter from the form
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        sid = request.form.get('studentid')
        uname = request.form.get('username')
        password = request.form.get('password')
        cpassword = request.form.get('confirmpassword')
        email = request.form.get('email')
        
        # get database connection
        connection = db.get_db()
        
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
            connection.commit()
            # close
            cur1.close()
            cur2.close()
            return "submitted"
    return render_template("r_test.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        uname = request.form.get('username', None)
        password = request.form.get('password', None)

        # get database connection
        connection = db.get_db()
        
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
            return redirect(url_for('user.profile'))

    return render_template("login.html")

@bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop('user_id')
    return redirect(url_for('user.login'))

@bp.route("/profile")
def profile():
    if not g.user:
        return redirect(url_for('user.login'))
    return render_template("profile.html")

@bp.route("/test")
def test():
    connection = db.get_db()
    q = "INSERT INTO userAccounts (userpassword, username, useremail, isStudent, isProf, isSysop, isAdmin, isTA)\
    VALUES ('a', 'b', 'c', ?, 0, 0, 0, 0)"
    cur2 = connection.execute(q, (None,))
    connection.commit()
    # close
    cur2.close()
    return 'done'


