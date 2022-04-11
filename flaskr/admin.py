from ctypes.wintypes import tagSIZE
from dis import dis
import os
import sqlite3
from tkinter.messagebox import NO
from traceback import print_tb
import traceback
from flask import Blueprint, render_template, request, flash, Markup, current_app
from numpy import disp
import pandas
from flaskr import db

bp = Blueprint("admin",__name__,template_folder="templates", url_prefix="/")

@bp.route('admin/info', methods=["GET","POST"]) 
def info():
    if request.method == "POST":
        func = request.form.get("submit")
        if (func == "Search TA"):
            # user input
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
 
                # student rating average (per course per term)
                query = "select r.term, r.coursenum, avg(r.score) from studenttarating r where tid ='{}' group by r.term, r.coursenum order by r.term desc, r.coursenum".format(tid)
                cur.execute(query)
                ratings = cur.fetchall() 
                if (len(ratings) > 0):
                    dispr = True
                else:
                    dispr = False    

                # student comments
                query = "select term, coursenum, comments from studenttarating r where tid='{}' order by r.term, r.coursenum".format(tid)
                cur.execute(query)
                comments = cur.fetchall()
                if (len(comments) > 0):
                    dispc = True
                else:
                    dispc = False

                # professor performance log
                query = "select t.term, t.coursenum, c.instructor, t.comments from talog t join courses c on t.term = c.term and t.coursenum = c.coursenum where tid='{}' order by t.term desc, t.coursenum".format(tid)
                cur.execute(query)
                log = cur.fetchall()
                if (len(log) > 0):
                    displ = True
                else:
                    displ = False     

                # prof wishlist
                query = "select w.term, w.coursenum, c.instructor from wishlist w join courses c on w.term = c.term and w.coursenum = c.coursenum where tid='{}' order by w.term desc, w.coursenum".format(tid)
                cur.execute(query)
                wishlist = cur.fetchall() 
                if (len(wishlist) > 0):
                    dispw = True
                else:
                    dispw = False 

                # courses assigned
                query = "select term, coursenum from taassignment a where tid= '{}' order by a.term desc".format(tid)
                cur.execute(query)
                courses = cur.fetchall()
                if (len(courses) > 0):
                    dispa = True
                else:
                    dispa = False

            except Exception as e:
                print(traceback.format_exc())
        return render_template("info.html", dispr=dispr, dispc=dispc, dispa=dispa, displ=displ, dispw=dispw, cohort=cohort, ratings=ratings, comments=comments, log=log, wishlist=wishlist, courses=courses)
    return render_template("info.html")

@bp.route('admin/courseinfo', methods=["GET","POST"]) 
def courseinfo():
    if request.method == "POST":
        func = request.form.get("submit")
        if (func == "Search Course"):
            # user input
            term = request.form.get("term_month_year")
            coursenum = request.form.get("coursenum")

            # get database connection
            con = db.get_db()   
            cur = con.cursor()
            con.row_factory = sqlite3.Row

            try: 
                # get TA Quota
                query = "select taquota from courses where coursenum='{}' and term='{}'".format(coursenum, term)
                cur.execute(query)
                res = cur.fetchone()
                if (res == None):
                    flash(Markup("<font color=\"red\">No TA Quota assoicated with {}. Please validate course data.</font>").format(coursenum))
                    return render_template("courseinfo.html")
                taquota = cur.fetchone()[0]
                
                # get current number of TA
                query = "select count(*) from taassignment where term='{}' and coursenum='{}' and active = 1 group by term, coursenum union select 0 where not exists (select * from taassignment where coursenum='{}' and term='{}')".format(term, coursenum, coursenum, term)
                cur.execute(query)
                curta = cur.fetchone()[0]

                fillrate = curta / taquota     # Filled Rate = enrollment_num / quota

                # all TA assigned to the course (current and past)            
                query = "select a.tid, c.tname from taassignment a join tacohort c on a.tid = c.tid and a.term = c.term where a.coursenum= '{}' and a.term='{}' and a.active = 1 order by a.term desc".format(coursenum, term)
                cur.execute(query)
                tas = cur.fetchall() 
                if (len(tas) > 0):  # found at least 1 TA
                    disp = True
                    dispn = True
                else:
                    disp = False
                    dispn = True
                    return render_template("courseinfo.html", disp=disp, dispn=dispn, term=term, course=coursenum, curta=curta, taquota=taquota, fillrate=fillrate)
            except Exception as e:
                print(traceback.format_exc())
                flash(Markup("<font color=\"red\">Error: Please validate your input.</font>"))
                return render_template("courseinfo.html")
        return render_template("courseinfo.html", disp=disp, dispn=dispn, term=term, course=coursenum, curta=curta, taquota=taquota, fillrate=fillrate, tas=tas)
    return render_template("courseinfo.html")

@bp.route('admin/update', methods=["GET","POST"]) 
def update():
    if request.method == "POST":
        func = request.form.get("submit")
        
        if (func == "search"):   # list all TA
            # user input
            term = request.form.get("term_month_year")
            course = request.form.get("course_num")

            # get database connection
            con = db.get_db()
            cur = con.cursor()
            con.row_factory = sqlite3.Row

            try:
                # get TA Quota
                query = "select taquota from courses where coursenum='{}' and term='{}'".format(course, term)
                cur.execute(query)
                res = cur.fetchone()
                if (res == None):
                    flash(Markup("<font color=\"red\">No TA Quota assoicated with {}. Please validate course data.</font>").format(course))
                    return render_template("courseinfo.html")
                taquota = res[0]
                
                # get current number of TA
                query = "select count(*) from taassignment where term='{}' and coursenum='{}' and active = 1 group by term, coursenum union select 0 where not exists (select * from taassignment where coursenum='{}' and term='{}')".format(term, course, course, term)
                cur.execute(query)
                curta = cur.fetchone()[0]

                # Filled Rate = enrollment_num / quota
                fillrate = curta / taquota

                # get current assigned TAs
                cur.execute("select t.tname, t.tid, t.hours from tacohort t join taassignment a on t.tid = a.tid and t.term = a.term where a.active = true and a.term=:term and a.coursenum=:course", {"term": term, "course": course})
                tas = cur.fetchall()
                if (len(tas) > 0):  # found at least 1 TA
                    disp = True
                    dispn = True
                else:
                    disp = False
                    dispn = True
                    return render_template("update.html", disp=disp, dispn=dispn, term=term, course=course, curta=curta, taquota=taquota, fillrate=fillrate)
            except Exception as e:
                print(traceback.format_exc())
                flash(Markup("<font color=\"red\">Error: Search Failed. Please validate input data.</font>"))
                return render_template("update.html")
            return render_template("update.html", disp=disp, dispn=dispn, term=term, course=course, curta=curta, taquota=taquota, fillrate=fillrate, data=tas)
            
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

        elif (func == "update"):    # update hours for a TA
            # user input
            term = request.form.get("term_month_year")
            tid = request.form.get("tid")
            hours = request.form.get("hours")

            # get database connection
            con = db.get_db()
            cur = con.cursor()
            try:
                query = "update tacohort set hours = '{}' where term='{}' and tid='{}'".format(hours, term, tid)
                cur.execute(query)
                con.commit()
                if (cur.rowcount == 1):
                    flash(Markup("<font color=\"green\">Update Hours Successful!</font>"))
                else:
                    flash(Markup("<font color=\"red\">Error: Update Hours Failed. Please validate input data.</font>"))
            except Exception as e:
                print(str(e))
                flash(Markup("<font color=\"red\">Error: Update Failed. Please validate input data.</font>"))
            return render_template("update.html")
    return render_template("update.html")

@bp.route('admin/adminimport', methods=["GET","POST"]) 
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

        # bonus features
        elif (func == "Upload Ugrad TA Info"):
            # get uploaded file from POST
            file = request.files["fileUploadU"]
            if file.filename.endswith(".csv"):
                file_path = os.path.join(current_app.root_path,current_app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                parseUgrad(file_path) # insert/ update data from CSV to DB
            else:
                flash(Markup("<font color=\"red\">Error: Please select and upload a valid .csv file</font>"))
                return render_template("adminimport.html")
        
        elif (func == "Upload Grad TA Info"):
            # get uploaded file from POST
            file = request.files["fileUploadG"]
            if file.filename.endswith(".csv"):
                file_path = os.path.join(current_app.root_path,current_app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                parseGrad(file_path) # insert/ update data from CSV to DB
            else:
                flash(Markup("<font color=\"red\">Error: Please select and upload a valid .csv file</font>"))
                return render_template("adminimport.html")
        
        elif (func == "Upload Historical Info"):
            # get uploaded file from POST
            file = request.files["fileUploadH"]
            if file.filename.endswith(".csv"):
                file_path = os.path.join(current_app.root_path,current_app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                parseHistory(file_path) # insert/ update data from CSV to DB
            else:
                flash(Markup("<font color=\"red\">Error: Please select and upload a valid .csv file</font>"))
                return render_template("adminimport.html")
    return render_template("adminimport.html")

@bp.route('dashboard')
def dashboard():
    return render_template("dashboard.html")

def parseQuota(filePath):
    try:
        # CSV Column Names
        col_names = ['term','coursenum', 'coursetype', 'coursename', 'instructor', 'enrollnum', 'taquota']
        # Use Pandas to parse the CSV file
        csvData = pandas.read_csv(filePath,names=col_names, skiprows=1)
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data format.</font>"))
        return
    try: 
        for i,row in csvData.iterrows():            # iterate through all rows
            values = getvalues(row)
            query = ("REPLACE INTO courses (term, coursenum,coursetype, coursename, instructor, enrollnum, taquota) values (?, ?, ?, ?, ?, ?, ?)")
            con = db.get_db()
            con.execute(query, values)
            con.commit()
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data.</font>"))
        return
    flash(Markup("<font color=\"green\">Upload TA Quota Successful!</font>"))

def parseCohort(filePath):
    try:
        # CSV Column Names
        col_names = ['term','tname', 'tid', 'legalname', 'email', 'ugrad', 'supervisor', 'priority', 'hours', 'applieddate', 'location', 'phone', 'degree', 'coursesapplied', 'flexible', 'notes']
        # Use Pandas to parse the CSV file
        csvData = pandas.read_csv(filePath,names=col_names, skiprows=1)
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data format.</font>"))
        return
    # Loop through the Rows
    try:
        for i,row in csvData.iterrows():            # iterate through all rows
            values = getvalues(row)
            query = ("REPLACE INTO tacohort (term, tname, tid, legalname, email, ugrad, supervisor, priority, hours, applieddate, location, phone, degree, coursesapplied, flexible, notes) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            con = db.get_db()
            con.execute(query, values)
            con.commit()
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data.</font>"))
        return
    flash(Markup("<font color=\"green\">Upload TA Cohort Successful!</font>"))

def parseUgrad(filePath):
    try:
        # CSV Column Names
        col_names = ['jobapp','studentid','legalname', 'mcgillemail', 'degreeyear', 'preferences', 'previous', 'legalworker', 'country', 'email', 'dateapplied', 'location', 'phone', 'field', 'numcoursesapplied', 'lastcourse', 'course1', 'course1unit', 'course2', 'course2unit', 'totalunits', 'assignment', 'recnotes', 'notes']
        # Use Pandas to parse the CSV file  
        csvData = pandas.read_csv(filePath,names=col_names, skiprows=1)
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data format.</font>"))
        return

    try:
        for i,row in csvData.iterrows():    # iterate through all rows
            values = getvalues(row)
            query = ("replace INTO taapplication (jobapp, studentid, legalname, mcgillemail, degreeyear, preferences, previous, legalworker, country, email, dateapplied, location, phone, field, numcoursesapplied, lastcourse, course1, course1unit, course2, course2unit, totalunits, assignment, recnotes, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            con = db.get_db()
            con.execute(query, values)
            con.commit()
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data.</font>"))
        return
    flash(Markup("<font color=\"green\">Upload Historical Statistics for Undergraduate TA Successful!</font>"))

def parseGrad(filePath):
    try:
        # CSV Column Names
        col_names = ['jobapp','studentid','legalname', 'mcgillemail', 'supervisor', 'priority', 'hrs180', 'previousworker', 'legalworker', 'country', 'email', 'dateapplied', 'location', 'phone', 'degreeyear', 'coursesapplied', 'flexible', 'field','expsummary', 'previous', 'numcoursesapplied', 'appin', 'lastcourse', 'course1', 'course1unit', 'course2', 'course2unit', 'totalunits', 'assignment', 'status', 'notes', 'diff']
        # Use Pandas to parse the CSV file
        csvData = pandas.read_csv(filePath,names=col_names, skiprows=1)
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data format.</font>"))
        return

    try: 
        for i,row in csvData.iterrows():            # iterate through all rows
            values = getvalues(row)
            query = ("REPLACE INTO taapplication (jobapp, studentid, legalname, mcgillemail, supervisor, priority, hrs180, previousworker,  legalworker, country, email, dateapplied, location, phone, degreeyear, coursesapplied, flexible, field, expsummary, previous, numcoursesapplied, appin, lastcourse, course1, course1unit, course2, course2unit, totalunits, assignment, status, notes, diff) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            con = db.get_db()
            con.execute(query, values)
            con.commit()
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data.</font>"))
        return
    flash(Markup("<font color=\"green\">Upload Historical Statistics for Graduate TA Successful!</font>"))

def parseHistory(filePath):
    try:
        # CSV Column Names
        col_names = ['idlu','term','coursenum', 'units', 'tname', 'degree', 'supervisor', 'id', 'email', 'feedback']
        # Use Pandas to parse the CSV file
        csvData = pandas.read_csv(filePath,names=col_names, skiprows=1)
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data format.</font>"))
        return
    try: 
        for i,row in csvData.iterrows():            # iterate through all rows
            values = getvalues(row)
            query = ("REPLACE INTO tahistory (idlu, term, coursenum, units, tname, degree, supervisor, id, email, feedback) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            con = db.get_db()
            con.execute(query, values)
            con.commit()
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data.</font>"))
        return
    flash(Markup("<font color=\"green\">Upload TA Info History Successful!</font>"))

# get values in each row
def getvalues(row):
    values = []
    for e in row:
        if (e == ''):   # null value for empty cells
            values.append(None)
        else:
            values.append(e)
    return values

# TODO:
# role!