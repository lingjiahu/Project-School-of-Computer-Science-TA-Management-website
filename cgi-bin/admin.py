import csv
import os
import sqlite3
from flask import Blueprint, render_template, request, flash, Markup, current_app, g, redirect, url_for
import pandas
import db

#bp = Blueprint("admin",__name__,template_folder="templates", url_prefix="/")

# TA Info
#@bp.route('admin/info', methods=["GET","POST"]) 
def info():
    if not g.user:
        return redirect(url_for('landing'))
    if not g.user.isAdmin:
        return redirect(url_for('dashboard'))

    if request.method == "POST":
        func = request.form.get("submit")
        if (func == "Search TA"):
            # user input
            tid = request.form.get("tid")
            if (tid == ''):     # empty user input
                flash(Markup("<font color=\"red\">Error: TA Student ID cannot be empty. Please validate your input.</font>"))
                return render_template("info.html")
            else:
                values = [tid]

            try:
                # get database connection
                con = db.get_db()   
                cur = con.cursor()
                con.row_factory = sqlite3.Row

                # TA Cohort info (current and past)
                query = ("select * from tacohort where tid = ? order by term desc")
                cur.execute(query, values)
                cohort = cur.fetchall()

                # No TA record info found
                if (len(cohort) == 0):
                    flash(Markup("<font color=\"red\">Error: No record found. Please validate your input.</font>"))
                    return render_template("info.html")
 
                # student rating average (per course per term)
                query = "select r.term, r.coursenum, avg(r.score) from studenttarating r where tid ='{}' group by r.term, r.coursenum order by r.term desc, r.coursenum".format(tid)
                cur.execute(query)
                ratings = cur.fetchall() 
                if (len(ratings) > 0):
                    dispr = True    # display flag for student ratings
                else:
                    dispr = False

                # student comments
                query = "select term, coursenum, comments from studenttarating r where tid='{}' order by r.term, r.coursenum".format(tid)
                cur.execute(query)
                comments = cur.fetchall()
                if (len(comments) > 0):
                    dispc = True    # display flag for student comments
                else:
                    dispc = False

                # professor performance log
                query = "select t.term, t.coursenum, c.instructor, t.comments from talog t join courses c on t.term = c.term and t.coursenum = c.coursenum where tid='{}' order by t.term desc, t.coursenum".format(tid)
                cur.execute(query)
                print(query)
                log = cur.fetchall()
                if (len(log) > 0):
                    displ = True    # display flag for performance log
                else:
                    displ = False     

                # prof wishlist
                query = "select w.term, w.coursenum, c.instructor from wishlist w join courses c on w.term = c.term and w.coursenum = c.coursenum where tid='{}' order by w.term desc, w.coursenum".format(tid)
                cur.execute(query)
                wishlist = cur.fetchall() 
                if (len(wishlist) > 0):
                    dispw = True       # display flag for prof wishlist
                else:
                    dispw = False 

                # courses assigned
                query = "select term, coursenum from taassignment a where tid= '{}' order by a.term desc".format(tid)
                cur.execute(query)
                courses = cur.fetchall()
                if (len(courses) > 0):
                    dispa = True    # display flag for courses
                else:
                    dispa = False
            except Exception as e:
                print(e)
                flash(Markup("<font color=\"red\">Error: Please validate your input.</font>"))
                return render_template("info.html")
            
            return render_template("info.html", dispr=dispr, dispc=dispc, dispa=dispa, displ=displ, dispw=dispw, cohort=cohort, ratings=ratings, comments=comments, log=log, wishlist=wishlist, courses=courses)
    return render_template("info.html")
info.methods=["GET", "POST"]

# Course TA Info
#@bp.route('admin/courseinfo', methods=["GET","POST"]) 
def courseinfo():
    if not g.user:
        return redirect(url_for('landing'))
    if not g.user.isAdmin:
        return redirect(url_for('dashboard'))

    if request.method == "POST":
        func = request.form.get("submit")
        if (func == "Search Course"):
            # user input
            term = request.form.get("term_month_year")
            coursenum = request.form.get("coursenum")
            if (term == '' or coursenum == ''):     # empty user input
                flash(Markup("<font color=\"red\">Error: Term and Course cannot be empty. Please validate your input.</font>"))
                return render_template("courseinfo.html")

            # get database connection
            con = db.get_db()   
            cur = con.cursor()
            con.row_factory = sqlite3.Row

            try: 
                # get TA Quota
                query = "select taquota from courses where coursenum='{}' and term='{}'".format(coursenum, term)
                cur.execute(query)
                res = cur.fetchone()
                if (res == None):   # No record for the course
                    flash(Markup("<font color=\"red\"> No record found for {} {}. Please validate course data.</font>").format(coursenum, term))
                    return render_template("courseinfo.html")
                taquota = res[0]
                
                # get current number of TA
                query = "select count(*) from taassignment where term='{}' and coursenum='{}' and active = 1 group by term, coursenum union select 0 where not exists (select * from taassignment where coursenum='{}' and term='{}')".format(term, coursenum, coursenum, term)
                cur.execute(query)
                curta = cur.fetchone()[0]
                if (taquota == None):   # No valid TA Quota
                    taquota = "N/A"
                    fillrate = "N/A"
                else:             
                    fillrate = curta / taquota     # Filled Rate = enrollment_num / quota
                dispn = True    # display flag for relevant stats

                # all TA assigned to the course (current and past)            
                query = "select a.tid, c.tname from taassignment a join tacohort c on a.tid = c.tid and a.term = c.term where a.coursenum= '{}' and a.term='{}' and a.active = 1 order by a.term desc".format(coursenum, term)
                cur.execute(query)
                tas = cur.fetchall() 
                if (len(tas) > 0):  # found at least 1 TA
                    disp = True     # display flag for TAs
                else:   # tables of TAs not displayed
                    disp = False
                    return render_template("courseinfo.html", disp=disp, dispn=dispn, term=term, course=coursenum, curta=curta, taquota=taquota, fillrate=fillrate)
            except Exception as e:
                print(e)
                flash(Markup("<font color=\"red\">Error: Please validate your input.</font>"))
                return render_template("courseinfo.html")
        return render_template("courseinfo.html", disp=disp, dispn=dispn, term=term, course=coursenum, curta=curta, taquota=taquota, fillrate=fillrate, tas=tas)
    return render_template("courseinfo.html")
courseinfo.methods=["GET", "POST"]

# Update TA Info
#@bp.route('admin/update', methods=["GET","POST"]) 
def update():
    if not g.user:
        return redirect(url_for('landing'))
    if not g.user.isAdmin:
        return redirect(url_for('dashboard'))

    if request.method == "POST":
        func = request.form.get("submit")
        
        if (func == "Search"):   # list all TA
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
                if (res == None):   # No record for the course
                    flash(Markup("<font color=\"red\"> No record found for {} {}. Please validate course data.</font>").format(course, term))
                    return render_template("update.html")
                taquota = res[0]
                
                # get current number of TA
                query = "select count(*) from taassignment where term='{}' and coursenum='{}' and active = 1 group by term, coursenum union select 0 where not exists (select * from taassignment where coursenum='{}' and term='{}')".format(term, course, course, term)
                cur.execute(query)
                curta = cur.fetchone()[0]
                if (taquota == None):   # No valid TA Quota
                    taquota = "N/A"
                    fillrate = "N/A"
                else:             
                    fillrate = curta / taquota     # Filled Rate = enrollment_num / quota
                dispn = True    #display flag for relevant stats

                # get current assigned TAs
                cur.execute("select t.tname, t.tid, t.hours from tacohort t join taassignment a on t.tid = a.tid and t.term = a.term where a.active = true and a.term=:term and a.coursenum=:course", {"term": term, "course": course})
                tas = cur.fetchall()
                if (len(tas) > 0):  # found at least 1 TA
                    disp = True     # display flag for TAs
                else:   # tables of TAs not displayed
                    disp = False
                    return render_template("update.html", disp=disp, dispn=dispn, term=term, course=course, curta=curta, taquota=taquota, fillrate=fillrate)
            except Exception as e:
                print(e)
                flash(Markup("<font color=\"red\">Error: Search Failed. Please validate input data.</font>"))
                return render_template("update.html")
            return render_template("update.html", disp=disp, dispn=dispn, term=term, course=course, curta=curta, taquota=taquota, fillrate=fillrate, data=tas)
            
        elif (func == "Add"): # add a TA
            # user input
            term = request.form.get("term_month_year")
            course = request.form.get("course_num")
            tid = request.form.get("tid")
            values = []
            inputs=[term, course, tid]
            for e in inputs:
                if (e == ''):   # null value for empty cells
                    flash(Markup("<font color=\"red\">Error: Term, Course and TA Student ID cannot be empty. Please validate your input.</font>"))
                    return render_template("update.html")
                else:
                    values.append(e)

            # get database connection
            con = db.get_db()
            cur = con.cursor()
            con.row_factory = sqlite3.Row

            try:
                # validate input - TA
                tavalues = [values[0], values[2]]
                query = "select * from tacohort where term = ? and tid = ?"
                cur.execute(query, tavalues)
                res = cur.fetchall()
                if (len(res) == 0):
                    flash(Markup("<font color=\"red\">Error: No record associated with the TA Student ID {} in {}. Please validate your input.</font>").format(tid, term))
                    return render_template("update.html")

                # validate input - Course
                coursevalues = [values[0], values[1]]
                query = "select * from courses where term = ? and coursenum = ?"
                cur.execute(query, coursevalues)
                res = cur.fetchall()
                if (len(res) == 0):
                    flash(Markup("<font color=\"red\">Error: No record associated with {} {}. Please validate your input.</font>").format(course, term))
                    return render_template("update.html")

                # add TA to a course
                query = ("insert into taassignment values (?, ?, ?, true)")
                cur.execute(query, values)
                con.commit()
                if (cur.rowcount == 1):
                    flash(Markup("<font color=\"green\">Add Successful!</font>"))
                else:
                    flash(Markup("<font color=\"red\">Error: Add Failed. Please validate input data.</font>"))
            except Exception as e:
                print(str(e))
                flash(Markup("<font color=\"red\">Error: Add Failed. Please validate input data.</font>"))
            return render_template("update.html")

        elif (func == "Remove"): # remove a TA (active = false)
            # user input
            term = request.form.get("term_month_year")
            course = request.form.get("course_num")
            tid = request.form.get("tid")
            values = []
            inputs=[term, course, tid]
            for e in inputs:
                if (e == ''):   # null value for empty cells
                    flash(Markup("<font color=\"red\">Error: Term, Course and TA Student ID cannot be empty. Please validate your input.</font>"))
                    return render_template("update.html")
                else:
                    values.append(e)

            # get database connection
            con = db.get_db()
            cur = con.cursor()
            try:
                # remove TA
                query = ("update taassignment set active = false where term = ? and coursenum = ? and tid = ? and active = 1")
                cur.execute(query, values)
                con.commit()
                if (cur.rowcount == 1):
                    flash(Markup("<font color=\"green\">Remove Successful!</font>"))
                else:
                    flash(Markup("<font color=\"red\">Error: Remove Failed. Please validate input data.</font>"))
            except Exception as e:
                print(str(e))
                flash(Markup("<font color=\"red\">Error: Remove Failed. Please validate input data.</font>"))
            return render_template("update.html")

        elif (func == "Update Hours"):    # update hours for a TA
            # user input
            term = request.form.get("term_month_year")
            tid = request.form.get("tid")
            hours = request.form.get("hours")
            values = []
            inputs=[hours, term, tid]
            for e in inputs:
                if (e == ''):   # null value for empty cells
                    flash(Markup("<font color=\"red\">Error: Term, TA Student ID and Hours cannot be empty. Please validate your input.</font>"))
                    return render_template("update.html")
                else:
                    values.append(e)

            # get database connection
            con = db.get_db()
            cur = con.cursor()
            try:
                query = ("update tacohort set hours = ? where term = ? and tid= ?")
                cur.execute(query, values)
                con.commit()
                if (cur.rowcount == 1):
                    flash(Markup("<font color=\"green\">Update Hours Successful!</font>"))
                else:
                    flash(Markup("<font color=\"red\">Error: Update Hours Failed. Please validate input data.</font>"))
            except Exception as e:
                print(str(e))
                flash(Markup("<font color=\"red\">Error: Update Hours Failed. Please validate input data.</font>"))
            return render_template("update.html")

        elif (func == "Update Name"):    # update name for a TA
            # user input
            term = request.form.get("term_month_year")
            tid = request.form.get("tid")
            name = request.form.get("newname")
            values = []
            inputs=[name, term, tid]
            for e in inputs:
                if (e == ''):   # null value for empty cells
                    flash(Markup("<font color=\"red\">Error: Term, TA Student ID and Name cannot be empty. Please validate your input.</font>"))
                    return render_template("update.html")
                else:
                    values.append(e)

            # get database connection
            con = db.get_db()
            cur = con.cursor()
            try:
                query = ("update tacohort set tname = ? where term = ? and tid= ?")
                cur.execute(query, values)
                con.commit()
                if (cur.rowcount == 1):
                    flash(Markup("<font color=\"green\">Update TA Name Successful!</font>"))
                else:
                    flash(Markup("<font color=\"red\">Error: Update TA Name Failed. Please validate input data.</font>"))
            except Exception as e:
                print(str(e))
                flash(Markup("<font color=\"red\">Error: Update TA Name Failed. Please validate input data.</font>"))
            return render_template("update.html")
        
        elif (func == "Update Term"):    # update term for a TA
            # user input
            tid = request.form.get("tid")
            oldterm = request.form.get("oldterm")
            newterm = request.form.get("newterm")
            values = []
            inputs=[newterm, oldterm, tid]
            for e in inputs:
                if (e == ''):   # null value for empty cells
                    flash(Markup("<font color=\"red\">Error: TA Student ID, Old Term and New Term cannot be empty. Please validate your input.</font>"))
                    return render_template("update.html")
                else:
                    values.append(e)

            sdvalues = [values[2], values[1]]   # values for search and delete: tid, term   
            nvalues = [values[2], values[0]]    # values for constraint checking

            # get database connection
            con = db.get_db()
            cur = con.cursor()

            try:
                # check if old record exists
                query = "select * from tacohort where tid = ? and term = ?"
                cur.execute(query, sdvalues)
                res = cur.fetchall()
                if (len(res) == 0):
                    flash(Markup("<font color=\"red\">Error: No record associated with the TA Student ID {} in {}. Please validate your input.</font>").format(tid, oldterm))
                    return render_template("update.html")
                
                # check unique constraint on term and tid
                query = "select * from tacohort where tid = ? and term = ?"
                cur.execute(query, nvalues)
                res = cur.fetchall()
                if (len(res) != 0):
                    flash(Markup("<font color=\"red\">Error: Failed to update Term due to existing record for TA with Student ID {} in {}. Please validate your input.</font>").format(tid, newterm))
                    return render_template("update.html")

                # delete all relevant records
                # tables affected: taassignment, talog, studenttaratings, wishlist
                
                # delete records from taassignment
                query = "delete from taassignment where tid = ? and term = ?"
                cur.execute(query, sdvalues)
                if (cur.rowcount != 1):
                    flash(Markup("<font color=\"red\">Error: Update Term Failed. Please validate your input.</font>"))
                    return render_template("update.html")

                # delete records from talog
                query = "delete from talog where tid = ? and term = ?"
                cur.execute(query, sdvalues)

                # delete records from studenttaratings
                query = "delete from studenttarating where tid = ? and term = ?"
                cur.execute(query, sdvalues)

                # delete records from wishlist
                query = "delete from wishlist where tid = ? and term = ?"
                cur.execute(query, sdvalues)

                # update TA cohort
                query = ("update tacohort set term = ? where term = ? and tid= ?")
                cur.execute(query, values)
                con.commit()
                if (cur.rowcount == 1):
                    flash(Markup("<font color=\"green\">Update Term Successful!</font>"))
                else:
                    flash(Markup("<font color=\"red\">Error: Update Term Failed. Please validate input data.</font>"))

            except Exception as e:
                print(str(e))
                flash(Markup("<font color=\"red\">Error: Update Term Failed. Please validate input data.</font>"))
            return render_template("update.html")
    
        elif (func == "Update ID"):    # update ID for a TA
            # user input
            term = request.form.get("term")
            oldtid = request.form.get("oldid")
            newtid = request.form.get("newid")
            values = []
            inputs=[newtid, oldtid, term]
            for e in inputs:
                if (e == ''):   # null value for empty cells
                    flash(Markup("<font color=\"red\">Error: Term, Old TA Student ID and New TA Student ID cannot be empty. Please validate your input.</font>"))
                    return render_template("update.html")
                else:
                    values.append(e)

            sdvalues = [values[1], values[2]]   # values for search and delete: tid, term   
            nvalues = [values[0], values[2]]    # values for constraint checking

            # get database connection
            con = db.get_db()
            cur = con.cursor()

            try:
                # check if old record exists
                query = "select * from tacohort where tid = ? and term = ?"
                cur.execute(query, sdvalues)
                res = cur.fetchall()
                if (len(res) == 0):
                    flash(Markup("<font color=\"red\">Error: No record associated with the TA Student ID {} in {}. Please validate your input.</font>").format(oldtid, term))
                    return render_template("update.html")
                
                # check unique constraint on term and tid
                query = "select * from tacohort where tid = ? and term = ?"
                cur.execute(query, nvalues)
                res = cur.fetchall()
                if (len(res) != 0):
                    flash(Markup("<font color=\"red\">Error: Failed to update Term due to existing record for TA with Student ID {} in {}. Please validate your input.</font>").format(newtid, term))
                    return render_template("update.html")

                # delete all relevant records
                # tables affected: taassignment, talog, studenttaratings, wishlist
                
                # delete records from taassignment
                query = "delete from taassignment where tid = ? and term = ?"
                cur.execute(query, sdvalues)
                if (cur.rowcount != 1):
                    flash(Markup("<font color=\"red\">Error: Update Term Failed. Please validate your input.</font>"))
                    return render_template("update.html")

                # delete records from talog
                query = "delete from talog where tid = ? and term = ?"
                cur.execute(query, sdvalues)

                # delete records from studenttaratings
                query = "delete from studenttarating where tid = ? and term = ?"
                cur.execute(query, sdvalues)

                # delete records from wishlist
                query = "delete from wishlist where tid = ? and term = ?"
                cur.execute(query, sdvalues)

                query = ("update tacohort set tid = ? where tid = ? and term= ?")
                cur.execute(query, values)
                con.commit()
                if (cur.rowcount == 1):
                    flash(Markup("<font color=\"green\">Update TA Student ID Successful!</font>"))
                else:
                    flash(Markup("<font color=\"red\">Error: Update TA Student ID Failed. Please validate input data.</font>"))

            except Exception as e:
                print(str(e))
                flash(Markup("<font color=\"red\">Error: Update TA Student ID Failed. Please validate input data.</font>"))
            return render_template("update.html")
    return render_template("update.html")
update.methods=["GET", "POST"]

#@bp.route('admin/adminimport', methods=["GET","POST"]) 
def adminimport():
    if not g.user:
        return redirect(url_for('landing'))
    if not g.user.isAdmin:
        return redirect(url_for('dashboard'))

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
adminimport.methods=["GET", "POST"]

def parseQuota(filePath):
    try:
        # read CSV
        file = open(filePath)
        csvData = csv.reader(file)
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data format.</font>"))
        return
    try: 
        firstrow = True
        for row in csvData:            # iterate through all rows
            if (firstrow):              # skip first row (column names)
                firstrow = False
                continue
            if not len(row) == 0:   # skip empty rows
                values = getvalues(row)
            query = ("REPLACE INTO courses (term, coursenum,coursetype, coursename, instructor, enrollnum, taquota) values (?, ?, ?, ?, ?, ?, ?)")
            con = db.get_db()
            con.execute(query, values)
        con.commit()
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data.</font>"))
        return
    flash(Markup("<font color=\"green\">Upload Course Quota Successful!</font>"))

def parseCohort(filePath):
    try:
        # read CSV
        file = open(filePath)
        csvData = csv.reader(file)
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data format.</font>"))
        return
    # Loop through the Rows
    try:
        firstrow = True
        for row in csvData:            # iterate through all rows
            if (firstrow):              # skip first row (column names)
                firstrow = False
                continue
            if not len(row) == 0:   # skip empty rows
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
        # read CSV
        file = open(filePath)
        csvData = csv.reader(file)
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data format.</font>"))
        return

    try:
        firstrow = True
        for row in csvData:            # iterate through all rows
            if (firstrow):              # skip first row (column names)
                firstrow = False
                continue
            if not len(row) == 0:   # skip empty rows
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
        # read CSV
        file = open(filePath)
        csvData = csv.reader(file)
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data format.</font>"))
        return

    try: 
        firstrow = True
        for row in csvData:            # iterate through all rows
            if (firstrow):              # skip first row (column names)
                firstrow = False
                continue
            if not len(row) == 0:   # skip empty rows
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
        # read CSV
        file = open(filePath)
        csvData = csv.reader(file)
    except Exception as e:
        print(str(e))
        flash(Markup("<font color=\"red\">Error: Upload Failed. Please validate input data format.</font>"))
        return
    try: 
        firstrow = True
        for row in csvData:            # iterate through all rows
            if (firstrow):              # skip first row (column names)
                firstrow = False
                continue
            if not len(row) == 0:   # skip empty rows
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