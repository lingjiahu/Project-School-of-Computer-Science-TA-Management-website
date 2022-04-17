import os
from flask import Flask, Blueprint, render_template, request, url_for, flash, Markup, current_app
import pandas
import csv
import smtplib, ssl
from email.message import EmailMessage
import db

#@bp.route('/management', methods=["GET","POST"])
def management():
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

            if lastname=="" or firstname =="" or username == "" or pw == "" or (student=="0" and prof=="0" and sysop=="0" and admin=="0" and ta=="0" ):
                flash(Markup("<font color=\"red\">Error: <i>Firstname</i>, <i>Lastname</i>, <i>Username</i>, <i>Password</i> and <i>Login as</i> cannot be empty</font>"),"error")
                return render_template("management.html")

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
                #flash(Markup("<font color=\"red\">Error: Username already exists</font>"),"error")
                flash(Markup("<font color=\"red\">Error: {}</font>".format(str(e))),"error")
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
                return render_template("management.html")

            # get database connection
            con = db.get_db()

            # check if user exists
            cur1 = con.execute("SELECT * FROM userAccounts WHERE username='{}'".format(username))
            result = cur1.fetchall()
            if(not result):
                flash(Markup("<font color=\"red\">Error: Username doesn't exist</font>"),"error")
                return render_template("management.html")

            # update userpassword if password is not empty 
            if pw != "":
                query = ("UPDATE userAccounts SET userpassword = '{}' "
                "WHERE username='{}'").format(pw,username)
                try:
                    con.execute(query)
                    con.commit()
                except Exception as e:
                    print(str(e))
                    return render_template("management.html")

            # update useremail if email is not empty 
            if email != "":
                query = ("UPDATE userAccounts SET useremail = '{}' "
                "WHERE username='{}'").format(email,username)
                try:
                    con.execute(query)
                    con.commit()
                except Exception as e:
                    print(str(e))
                    return render_template("management.html")

            # update roles if roles are not empty 
            if student=="1" or prof=="1" or sysop=="1" or admin=="1" or ta=="1":
                query = ("UPDATE userAccounts SET isStudent = {}, isProf = {}, isSysop = {}, isAdmin = {}, isTA = {} "
                "WHERE username='{}'").format(student,prof,sysop,admin,ta,username)
                try:
                    con.execute(query)
                    con.commit()
                except Exception as e:
                    print(str(e))
                    return render_template("management.html")

            # update firstname if firstname is not empty 
            if firstname != "":
                query = ("UPDATE users SET firstname = '{}' "
                "WHERE username='{}'").format(firstname,username)
                try:
                    con.execute(query)
                    con.commit()
                except Exception as e:
                    print(str(e))
                    return render_template("management.html")

            # update lastname if lastname is not empty 
            if lastname != "":
                query = ("UPDATE users SET lastname = '{}' "
                "WHERE username='{}'").format(lastname,username)
                try:
                    con.execute(query)
                    con.commit()
                except Exception as e:
                    print(str(e))
                    return render_template("management.html")

            # update studentid if studentid is not empty 
            if studentid != "":
                query = ("UPDATE users SET studentid = {} "
                "WHERE username='{}'").format(studentid,username)
                try:
                    con.execute(query)
                    con.commit()
                except Exception as e:
                    print(str(e))
                return render_template("management.html")

            flash(Markup("Edit User <i>{}</i> successfully".format(username)))
            if result[0]['useremail'] != 'NULL':
                sendEmail("edit",username,result[0]['useremail'])
            
        elif func == "Remove":
            # get username that need to delete from POST
            username = request.form.get("username")

            # get database connection
            con = db.get_db()

            # username is needed to remove
            if username == "":
                flash(Markup("<font color=\"red\">Error: <i>Username</i> is needed to remove</font>"),"error")
                return render_template("management.html")

            # check if user exists
            cur = con.execute("SELECT * FROM userAccounts WHERE username='{}'".format(username))
            result = cur.fetchall()
            if(not result):
                flash(Markup("<font color=\"red\">Error: Username doesn't exist</font>"),"error")
                return render_template("management.html")
            # create query
            query = "DELETE FROM userAccounts WHERE username='{}'".format(username)
            query2 = "DELETE FROM users WHERE username='{}'".format(username)
            
            try:
                con.execute(query)
                con.execute(query2)
                con.commit()
            except Exception as e:
                print(str(e))
                return render_template("management.html")

            flash(Markup("Remove User <i>{}</i> successfully".format(username)))
            if result[0]['useremail'] != 'NULL':
                # remov is correct, do not add 'e' at the end
                sendEmail("remov",username,result[0]['useremail'])
            
    
    # out = sp.run(["php","sysop.php"],stdout=sp.PIPE)
    # return out.stdout
    return render_template("management.html")
managerment.methods=["GET", "POST"]

#@bp.route('/importcsv', methods=["GET","POST"])
def importcsv():
    if request.method == "POST":
        func = request.form.get("submit")
        print(func)

        if func == "Upload":
            
            # get uploaded file from POST
            file = request.files["fileUpload"]
            print("here")
            if file.filename.endswith(".csv"):
                file_path = os.path.join(current_app.root_path,current_app.config['UPLOAD_FOLDER'], file.filename)
                print(file_path)
                file.save(file_path)
                parseCSV(file_path)
            else:
                flash(Markup("<font color=\"red\">Error: Please select and upload a valid .csv file</font>"),"error")
                return render_template("import.html")
            
            flash(Markup("Import <i>{}</i> successfully".format(file.filename)))
    return render_template("import.html")
importcsv.methods=["GET", "POST"]

#@bp.route('/inputcourses', methods=["GET","POST"])
def inputcourses():
    if request.method == "POST":
        func = request.form.get("submit")
        print(func)
        if func == "Submit":
            # get infos for a course from POST
            term = request.form.get("term_month_year")
            coursenum = request.form.get("course_num")
            coursename = request.form.get("course_name")
            instructor = request.form.get("instructor_assigned_name")

            # course infos should not be empty
            if term == "" or coursenum == "" or coursename == "" or instructor == "":
                flash(Markup("<font color=\"red\">Error: Please fill all the blanks to submit a course</font>"),"error")
                return render_template("input.html")

            # get database connection
            con = db.get_db()
            # create query depends on input infos
            query = ("INSERT INTO courses (term,coursenum, " 
            "coursename, instructor) values"
            "('{}','{}','{}','{}')").format(term,coursenum,coursename, instructor)

            print(query)
            # execute query
            try:
                con.execute(query)
                con.commit()
                flash(Markup("Add Course <i>{}</i> successfully".format(coursenum)))
            except Exception as e:
                print(str(e))
                #flash(Markup("<font color=\"red\">Error: Course already exists</font>"),"error")
                flash(Markup("<font color=\"red\">Error: {}</font>".format(str(e))),"error")

    return render_template("input.html")
inputcourses.methods=["GET", "POST"]

def parseCSV(filePath):
    # CVS Column Names
    col_names = ['term','coursenum','coursename', 'instructor']
    # Use Pandas to parse the CSV file
    csvData = pandas.read_csv(filePath,names=col_names, header=None)
    # Loop through the Rows
    for i,row in csvData.iterrows():
        if i == 0:
            continue
        query = ("INSERT INTO courses (term,coursenum, " 
        "coursename, instructor) values"
        "('{}','{}','{}','{}')").format(row['term'],row['coursenum'],row['coursename'], row['instructor'])
        # get database connection
        con = db.get_db()
        try:
            con.execute(query)
            con.commit()
            print(i,query)
        except Exception as e:
            print(str(e))

def sendEmail(type,username,receiver_email):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    # enter sender email and password
    sender_email = ""
    password = ""

    msg = EmailMessage()
    
    message = """\
    Hi {},
    
    Your account has been {}ed.""".format(username,type)
    msg.set_content(message)

    msg['Subject'] = 'TA Management Website: Account Modified Notification'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.send_message(msg)
            server.quit()
    except Exception as e:
        print(str(e))