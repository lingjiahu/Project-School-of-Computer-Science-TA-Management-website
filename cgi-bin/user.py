import db
from flask import request, g, session, render_template, redirect, flash, url_for, redirect

def hello():
    return "index hello"

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
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect username or password. Try again.')

    return render_template("landing.html", visible=visible)
landing.methods=["GET", "POST"]

def register():
    color = "red"
    currentTerm = "Winter2022"
    connection = db.get_db()
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
register.methods=["GET", "POST"]

def logout():
    session.pop('user_id')
    return redirect(url_for('landing'))

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