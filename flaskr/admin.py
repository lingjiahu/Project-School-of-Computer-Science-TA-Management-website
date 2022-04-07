from fileinput import filename
import os
import sqlite3
from flask import Flask, Blueprint, render_template, request, url_for, flash, Markup, current_app
import pandas
from flaskr import db

bp = Blueprint("admin",__name__,url_prefix="/admin")

@bp.route('/info', methods=["GET","POST"]) 
def info():
    return render_template("info.html")

@bp.route('/update', methods=["GET","POST"]) 
def update():
    if request.method == "POST":
        func = request.form.get("submit")
        
        if (func == "search"):   # list all TA
            # user input
            term = request.form.get("term_month_year")
            course = request.form.get("course_num")

            # get database connection
            con = db.get_db()
            # query for data
            cur = con.cursor()
            cur.execute("select t.tname, t.tid, t.hours from tacohort t join taassignment a on t.tid = a.tid where a.term=:term and a.coursenum=:course", {"term": term, "course": course})
            con.row_factory = sqlite3.Row
            res = cur.fetchall()
            if (len(res) == 0):
                disp = 2
            else:
                disp = 1
            return render_template("update.html", data=res, disp=disp)
        elif (func == "add"): # add a TA
            # user input
            term = request.form.get("term_month_year")
            course = request.form.get("course_num")
            tid = request.form.get("tid")
            # get database connection
            con = db.get_db()
            cur = con.cursor()
            try:
                cur.execute("insert into taassignment (term, coursenum, tid) values (term=:term, coursenum=:course, tid=:tid)", {"term": term, "course": course, "tid": tid})
                con.commit()
                disp = 1
            except Exception as e:
                disp = 2
                print(str(e))
            return render_template("update.html", disp=disp)
        elif (func == "remove"): # remove a TA

            return render_template("update.html", disp=disp)
    return render_template("update.html")

# TODO
@bp.route('/adminimport', methods=["GET","POST"]) 
def adminimport():
    if request.method == "POST":
        func = request.form.get("submit")
        if func == "Upload Course Quota":
            # get uploaded file from POST
            file = request.files["fileUpload"]
            if file.filename.endswith(".csv"):
                print("succ")
                print(filename)
                file_path = os.path.join(current_app.root_path,current_app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                parseQuota(file_path)
            else:
                flash(Markup("<font color=\"red\">Error: Please select and upload a valid .csv file</font>"))
                return render_template("adminimport.html")
        elif (func == "Upload TA Cohort"):
            # get uploaded file from POST
            file = request.files["fileUpload"]
            if file.filename.endswith(".csv"):
                file_path = os.path.join(current_app.root_path,current_app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                parseCohort(file_path)
            else:
                print("fail")
                print(filename)
                flash(Markup("<font color=\"red\">Error: Please select and upload a valid .csv file</font>"))
                return render_template("adminimport.html")
    return render_template("adminimport.html")

def parseQuota(filePath):
    # CSV Column Names
    col_names = ['term','coursenum','coursename', 'instructor', 'coursetype', 'courseenrollnum', 'taquota']
    # Use Pandas to parse the CSV file
    csvData = pandas.read_csv(filePath,names=col_names, header=None)
    # Loop through the Rows
    for i,row in csvData.iterrows():
        # execute query
        query = ("INSERT INTO courses (term, coursenum, coursename, instructor, coursetype, courseenrollnum, taquota) values"
        "('{}','{}','{}','{}','{}','{}','{}')").format(row['term'],row['coursenum'],row['coursename'], row['instructor'], row['coursetype'], row['courseenrollnum'], row['taquota'])
        try: 
            con = db.get_db()
            con.execute(query)
            con.commit()
            flash(Markup("<font color=\"green\">Upload Successful!</font>"))
        except Exception as e:
            print(str(e))
            flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data.</font>"))

def parseCohort(filePath):
    # CSV Column Names
    col_names = ['term','tname', 'tid', 'legalname', 'email', 'ugrad', 'supervisor', 'priority', 'hours', 'applieddate', 'location', 'phone', 'degree', 'coursesapplied', 'flexible', 'notes']
    # Use Pandas to parse the CSV file
    csvData = pandas.read_csv(filePath,names=col_names, header=None)
    # Loop through the Rows
    for i,row in csvData.iterrows():
        query = ("INSERT INTO tacohort (term, tname, tid, legalname, email, ugrad, supervisor, priority, hours, applieddate, location, phone, degree, coursesapplied, flexible, notes)"
        "values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')").format(row['term'],row['tname'],row['tid'], row['legalname'],row['email'],row['ugrad'],row['supervisor'], row['priority'], row['hours'],row['applieddate'],row['location'],row['phone'],row['degree'],row['coursesapplied'],row['flexible'], row['notes'])
        # execute query
        try:
            con = db.get_db()
            con.execute(query)
            con.commit()
            flash(Markup("<font color=\"green\">Upload Successful!</font>"))
        except Exception as e:
            print(str(e))
            flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data.</font>"))