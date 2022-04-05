import os
import subprocess as sp
from flask import Flask, render_template, request, url_for, flash, Markup
import pandas
import csv
import smtplib, ssl
from email.message import EmailMessage

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
    
    @app.route('/', methods=["GET","POST"])
    def home():
        return "HelloWorld"


    @app.route('/sysop', methods=["GET","POST"])
    def sysop():
        if request.method == "POST":
            func = request.form.get("submit")
            print(func)
            if func == "Add":
                # get infos for a user from POST
                firstname = request.form.get("firstname")
                lastname = request.form.get("lastname")
                studentid = request.form.get("studentid")
                username = request.form.get("username")
                pw = request.form.get("password")
                email = request.form.get("email")
                # initialize roles
                student = "1"
                prof = "1"
                sysop = "1"
                admin = "1"
                ta = "1"
                # check if roles are selected
                if request.form.get("role1") is None:
                    student = "0"
                if request.form.get("role2") is None:
                    prof = "0"
                if request.form.get("role3") is None:
                    sysop = "0"
                if request.form.get("role4") is None:
                    admin = "0"
                if request.form.get("role5") is None:
                    ta = "0"

                if username == "" or pw == "" or (student=="0" and prof=="0" and sysop=="0" and admin=="0" and ta=="0"):
                    flash(Markup("<font color=\"red\">Error: <i>Username</i>, <i>Password</i> and <i>Login as</i> cannot be empty</font>"),"error")
                    return render_template("sysop.html")

                # get database connection
                con = db.get_db()
                # create query depends on input infos
                if email == "":
                    query = ("INSERT INTO userAccounts (username, " 
                    "userpassword, useremail, isStudent, isProf, isSysop, isAdmin, isTA) values"
                    "('{}','{}',NULL,{},{},{},{},{})").format(username,pw,student, prof, sysop, admin, ta)
                else:
                    query = ("INSERT INTO userAccounts (username, " 
                    "userpassword, useremail, isStudent, isProf, isSysop, isAdmin, isTA) values"
                    "('{}','{}','{}',{},{},{},{},{})").format(username,pw,email,student, prof, sysop, admin, ta)
                
                if studentid == "":
                    query2 = ("INSERT INTO users (firstname, " 
                    "lastname, studentId, username) values"
                    "('{}','{}',NULL,'{}')").format(firstname,lastname,username)
                else:
                    query2 = ("INSERT INTO users (firstname, " 
                    "lastname, studentId, username) values"
                    "('{}','{}',{},'{}')").format(firstname,lastname,studentid,username)
                print(query)
                # execute query
                try:
                    con.execute(query)
                    con.execute(query2)
                    con.commit()
                    flash(Markup("Add User <i>{}</i> successfully".format(username)))
                    if email != "":
                        sendEmail("add",username,email)
                except Exception as e:
                    print(str(e))
                    flash(Markup("<font color=\"red\">Error: Username already exists</font>"),"error")
            elif func == "Edit":
                # get infos for a user from POST
                firstname = request.form.get("firstname")
                lastname = request.form.get("lastname")
                studentid = request.form.get("studentid")
                username = request.form.get("username")
                pw = request.form.get("password")
                email = request.form.get("email")
                # initialize roles
                student = "1"
                prof = "1"
                sysop = "1"
                admin = "1"
                ta = "1"
                # check if roles are selected
                if request.form.get("role1") is None:
                    student = "0"
                if request.form.get("role2") is None:
                    prof = "0"
                if request.form.get("role3") is None:
                    sysop = "0"
                if request.form.get("role4") is None:
                    admin = "0"
                if request.form.get("role5") is None:
                    ta = "0"

                if username == "":
                    flash(Markup("<font color=\"red\">Error: <i>Username</i> is needed to edit</font>"),"error")
                    return render_template("sysop.html")

                # check if user exists
                result = query_db("SELECT * FROM userAccounts WHERE username='{}'".format(username),one=True)
                if(result is None):
                    flash(Markup("<font color=\"red\">Error: Username doesn't exist</font>"),"error")
                    return render_template("sysop.html")

                # get database connection
                con = db.get_db()
                # update userpassword if password is not empty 
                if pw != "":
                    query = ("UPDATE userAccounts SET userpassword = '{}' "
                    "WHERE username='{}'").format(pw,username)
                    try:
                        con.execute(query)
                        con.commit()
                    except Exception as e:
                        print(str(e))
                        return render_template("sysop.html")

                # update useremail if email is not empty 
                if email != "":
                    query = ("UPDATE userAccounts SET useremail = '{}' "
                    "WHERE username='{}'").format(email,username)
                    try:
                        con.execute(query)
                        con.commit()
                    except Exception as e:
                        print(str(e))
                        return render_template("sysop.html")

                # update roles if roles are not empty 
                if student=="1" or prof=="1" or sysop=="1" or admin=="1" or ta=="1":
                    query = ("UPDATE userAccounts SET isStudent = {}, isProf = {}, isSysop = {}, isAdmin = {}, isTA = {} "
                    "WHERE username='{}'").format(student,prof,sysop,admin,ta,username)
                    try:
                        con.execute(query)
                        con.commit()
                    except Exception as e:
                        print(str(e))
                        return render_template("sysop.html")

                # update firstname if firstname is not empty 
                if firstname != "":
                    query = ("UPDATE users SET firstname = '{}' "
                    "WHERE username='{}'").format(firstname,username)
                    try:
                        con.execute(query)
                        con.commit()
                    except Exception as e:
                        print(str(e))
                        return render_template("sysop.html")

                # update lastname if lastname is not empty 
                if lastname != "":
                    query = ("UPDATE users SET lastname = '{}' "
                    "WHERE username='{}'").format(lastname,username)
                    try:
                        con.execute(query)
                        con.commit()
                    except Exception as e:
                        print(str(e))
                        return render_template("sysop.html")

                # update studentid if studentid is not empty 
                if studentid != "":
                    query = ("UPDATE users SET studentid = {} "
                    "WHERE username='{}'").format(studentid,username)
                    try:
                        con.execute(query)
                        con.commit()
                    except Exception as e:
                        print(str(e))
                        return render_template("sysop.html")

                flash(Markup("Edit User <i>{}</i> successfully".format(username)))
                if result['useremail'] != 'NULL':
                    sendEmail("edit",username,result['useremail'])
                
            elif func == "Remove":
                # get username that need to delete from POST
                username = request.form.get("username")

                # username is needed to remove
                if username == "":
                    flash(Markup("<font color=\"red\">Error: <i>Username</i> is needed to remove</font>"),"error")
                    return render_template("sysop.html")

                # check if user exists
                result = query_db("SELECT * FROM userAccounts WHERE username='{}'".format(username),one=True)
                if(result is None):
                    flash(Markup("<font color=\"red\">Error: Username doesn't exist</font>"),"error")
                    return render_template("sysop.html")
                # create query
                query = "DELETE FROM userAccounts WHERE username='{}'".format(username)
                query2 = "DELETE FROM users WHERE username='{}'".format(username)
                # get database connection
                con = db.get_db()
                try:
                    con.execute(query)
                    con.execute(query2)
                    con.commit()
                except Exception as e:
                    print(str(e))
                    render_template("sysop.html")

                flash(Markup("Remove User <i>{}</i> successfully".format(username)))
                if result['useremail'] != 'NULL':
                    # remov is correct, do not add 'e' at the end
                    sendEmail("remov",username,result['useremail'])
                

            elif func == "Submit":
                # get infos for a course from POST
                term = request.form.get("term_month_year")
                courseNum = request.form.get("course_num")
                courseName = request.form.get("course_name")
                instructor = request.form.get("instructor_assigned_name")

                # course infos should not be empty
                if term == "" or courseNum == "" or courseName == "" or instructor == "":
                    flash(Markup("<font color=\"red\">Error: Please fill all the blanks to submit a course</font>"),"error")
                    return render_template("sysop.html")

                # get database connection
                con = db.get_db()
                # create query depends on input infos
                query = ("INSERT INTO courses (term,courseNum, " 
                "courseName, instructor) values"
                "('{}','{}','{}','{}')").format(term,courseNum,courseName, instructor)

                print(query)
                # execute query
                try:
                    con.execute(query)
                    con.commit()
                    flash(Markup("Add Course <i>{}</i> successfully".format(courseNum)))
                except Exception as e:
                    print(str(e))
                    flash(Markup("<font color=\"red\">Error: Course already exists</font>"),"error")

            elif func == "Upload":
                
                # get uploaded file from POST
                file = request.files["fileUpload"]
                print("here")
                if file.filename.endswith(".csv"):
                    file_path = os.path.join(app.root_path,app.config['UPLOAD_FOLDER'], file.filename)
                    print(file_path)
                    file.save(file_path)
                    parseCSV(file_path)
                else:
                    flash(Markup("<font color=\"red\">Error: Please select a .csv file first</font>"),"error")
                    return render_template("sysop.html")
                
                flash(Markup("Import <i>{}</i> successfully".format(file.filename)))
        
        # out = sp.run(["php","sysop.php"],stdout=sp.PIPE)
        # return out.stdout
        return render_template("sysop.html")

    return app

def parseCSV(filePath):
    # CVS Column Names
    col_names = ['term','courseNum','courseName', 'instructor']
    # Use Pandas to parse the CSV file
    csvData = pandas.read_csv(filePath,names=col_names, header=None)
    # Loop through the Rows
    for i,row in csvData.iterrows():
        query = ("INSERT INTO courses (term,courseNum, " 
        "courseName, instructor) values"
        "('{}','{}','{}','{}')").format(row['term'],row['courseNum'],row['courseName'], row['instructor'])
        # get database connection
        con = db.get_db()
        con.execute(query)
        con.commit()
        print(i,row['term'],row['courseNum'],row['courseName'],row['instructor'])

def sendEmail(type,username,receiver_email):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    # enter sender email and password
    sender_email = "xiaojieyiandy@gmail.com"
    password = "Andy06170504?"

    msg = EmailMessage()
    
    message = """\
    Hi {},
    
    Your account has been {}ed.""".format(username,type)
    msg.set_content(message)

    msg['Subject'] = 'TA Management Website: Account Modified Notification'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        
if __name__ == "__main__":
    app.run(debug=True)
