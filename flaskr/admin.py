import os
import sqlite3
from flask import Blueprint, render_template, request, flash, Markup, current_app
from numpy import disp
import pandas
from flaskr import db

bp = Blueprint("admin",__name__,url_prefix="/admin")

@bp.route('/info', methods=["GET","POST"]) 
def info():
    if request.method == "POST":
        func = request.form.get("submit")
        if (func == "Search TA"):
            # user input
            # TODO term = request.form.get("term") 
            tid = request.form.get("tid")
            
            try:
                # get database connection
                con = db.get_db()   
                cur = con.cursor()
                con.row_factory = sqlite3.Row

                # TA Cohort info (current and past)
                cur.execute("select * from tacohort where tid=:tid order by term desc", {"tid": tid})
                cohort = cur.fetchall()

                # No TA info found
                if (len(cohort) == 0):
                    flash(Markup("<font color=\"red\">Error: No record found. Please validate your input.</font>"))
                    return render_template("info.html")
 
                # student rating average
                # TODO
                # cur.execute("select ")
                # ratings = cur.fetchall()     

                # student comments
                query = "select comments from studenttarating where '{}'".format(tid)
                cur.execute(query)
                comments = cur.fetchall()
                if (len(comments) > 0):
                    dispc = True
                else:
                    dispc = False

                # professor performance log
                # TODO
                # query = "".format(tid)
                # cur.execute(query)
                # performlog = cur.fetchall()     

                # prof wishlist
                # TODO
                # cur.execute()
                # wishlist = cur.fetchall() 

                # courses assigned
                query = "select term, coursenum from taassignment where tid= '{}' order by term desc".format(tid)
                cur.execute(query)
                courses = cur.fetchall()
            except Exception as e:
                print(e)
        return render_template("info.html", dispc=dispc, cohort=cohort, comments=comments, courses=courses)
    return render_template("info.html")

@bp.route('/courseinfo', methods=["GET","POST"]) 
def courseinfo():
    if request.method == "POST":
        func = request.form.get("submit")
        if (func == "Search Course"):
            # user input
            coursenum = request.form.get("coursenum")
            
            # get database connection
            con = db.get_db()   
            cur = con.cursor()
            con.row_factory = sqlite3.Row

            # all TA assigned to the course (current and past)
            # cur.execute("select a.term, a.tid, c.tname from taassignment a join tacohort c on a.tid = c.tid where a.coursenum=:coursenum order by a.term desc", {"coursenum": coursenum})
            
            query = "select a.term, a.tid, c.tname from taassignment a join tacohort c on a.tid = c.tid where a.coursenum= '{}' order by a.term desc".format(coursenum)
            cur.execute(query)
            tas = cur.fetchall() 
            # No TA info found
            if (len(tas) == 0):
                flash(Markup("<font color=\"red\">Error: No record found. Please validate your input.</font>"))
                disp = False
            else:
                disp = True
            return render_template("courseinfo.html", disp=disp, course=coursenum, tas=tas)
  
        return render_template("courseinfo.html")
        
    return render_template("courseinfo.html")

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
            cur.execute("select t.tname, t.tid, t.hours from tacohort t join taassignment a on t.tid = a.tid where a.active = true and a.term=:term and a.coursenum=:course", {"term": term, "course": course})
            con.row_factory = sqlite3.Row
            res = cur.fetchall()
            if (len(res) == 0):
                disp = 1   # disp = 1: no record from search
            else:
                disp = 2   # disp = 2: >=1 record from search
            return render_template("update.html", term=term, course=course, data=res, disp=disp)
        elif (func == "add"): # add a TA
            # user input
            term = request.form.get("term_month_year")
            course = request.form.get("course_num")
            tid = request.form.get("tid")
            # get database connection
            con = db.get_db()
            cur = con.cursor()
            try:
                cur.execute(("replace into taassignment values ('{}','{}','{}', true)").format(term,course,tid))
                con.commit()
                flash(Markup("<font color=\"green\">Add Successful!</font>"))
            except Exception as e:
                print(str(e))
                flash(Markup("<font color=\"red\">Error: Add Failed. Please validate input data.</font>"))
            return render_template("update.html")
        elif (func == "remove"): # remove a TA (active = false)
            # user input
            term = request.form.get("term_month_year")
            course = request.form.get("course_num")
            tid = request.form.get("tid")
            # get database connection
            con = db.get_db()
            cur = con.cursor()
            try:
                cur.execute("update taassignment set active = false where term=:term and coursenum=:course and tid=:tid", {"term": term, "course": course, "tid": tid})
                con.commit()
                if (cur.rowcount == 1):
                    flash(Markup("<font color=\"green\">Remove Successful!</font>"))
                else:
                    flash(Markup("<font color=\"red\">Error: Remove Failed. Please validate input data.</font>"))
            except Exception as e:
                print(str(e))
                flash(Markup("<font color=\"red\">Error: Remove Failed. Please validate input data.</font>"))
            return render_template("update.html")
    return render_template("update.html")

@bp.route('/adminimport', methods=["GET","POST"]) 
def adminimport():
    if request.method == "POST":
        func = request.form.get("submit")
        if func == "Upload Course Quota":
            # get uploaded file from POST
            file = request.files["fileUploadCQ"]
            if file.filename.endswith(".csv"):
                file_path = os.path.join(current_app.root_path,current_app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                parseQuota(file_path) # insert/ update data from CSV to DB
            else:
                flash(Markup("<font color=\"red\">Error: Please select and upload a valid .csv file</font>"))
                return render_template("adminimport.html")
        elif (func == "Upload TA Cohort"):
            # get uploaded file from POST
            file = request.files["fileUploadC"]
            if file.filename.endswith(".csv"):
                file_path = os.path.join(current_app.root_path,current_app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                parseCohort(file_path) # insert/ update data from CSV to DB
            else:
                flash(Markup("<font color=\"red\">Error: Please select and upload a valid .csv file</font>"))
                return render_template("adminimport.html")
    return render_template("adminimport.html")

def parseQuota(filePath):
    try:
        # CSV Column Names
        col_names = ['term','coursenum','coursename', 'instructor', 'coursetype', 'courseenrollnum', 'taquota']
        # Use Pandas to parse the CSV file
        csvData = pandas.read_csv(filePath,names=col_names, header=None)
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data format.</font>"))
        return
    # Loop through the Rows
    for i,row in csvData.iterrows():
        # execute query
        try: 
            query = ("REPLACE INTO courses (term, coursenum, coursename, instructor, coursetype, courseenrollnum, taquota) values"
            "('{}','{}','{}','{}','{}','{}','{}')").format(row['term'],row['coursenum'],row['coursename'], row['instructor'], row['coursetype'], row['courseenrollnum'], row['taquota'])
            con = db.get_db()
            con.execute(query)
            con.commit()
            flash(Markup("<font color=\"green\">Upload Successful!</font>"))
        except Exception as e:
            print(str(e))
            flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data.</font>"))

def parseCohort(filePath):
    try:
    # CSV Column Names
        col_names = ['term','tname', 'tid', 'legalname', 'email', 'ugrad', 'supervisor', 'priority', 'hours', 'applieddate', 'location', 'phone', 'degree', 'coursesapplied', 'flexible', 'notes']
        # Use Pandas to parse the CSV file
        csvData = pandas.read_csv(filePath,names=col_names, header=None)
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data format.</font>"))
        return
    # Loop through the Rows
    for i,row in csvData.iterrows():
        # execute query
        try:
            query = ("REPLACE INTO tacohort (term, tname, tid, legalname, email, ugrad, supervisor, priority, hours, applieddate, location, phone, degree, coursesapplied, flexible, notes)"
            "values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')").format(row['term'],row['tname'],row['tid'], row['legalname'],row['email'],row['ugrad'],row['supervisor'], row['priority'], row['hours'],row['applieddate'],row['location'],row['phone'],row['degree'],row['coursesapplied'],row['flexible'], row['notes'])
            con = db.get_db()
            con.execute(query)
            con.commit()
            flash(Markup("<font color=\"green\">Upload Successful!</font>"))
        except Exception as e:
            print(str(e))
            flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data.</font>"))


# TODO:
# update header/ footer: overlap when resizing, footer covers text
# change info to tainfo
# test descending order query