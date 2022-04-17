import os
from flask import Flask, Blueprint,redirect, render_template, request, url_for, flash, Markup, current_app
import pandas
import csv
import smtplib, ssl
from . import db

bp = Blueprint("ta_management",__name__,url_prefix="/ta_management")

@bp.route('/choose_course', methods=["GET","POST"])
def choose_course():

    # get database connection
    con = db.get_db()
    cur = con.execute("SELECT * FROM courses")
    rv = cur.fetchall()
    for course in rv:
        flash(Markup("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><tr>".format(course['term'],course['courseNum'],course['courseName'],course['instructor'])),"courses")
    
    if request.method == "POST":
        func = request.form.get("submit")
        print(func)
        if func == "ChooseCourse":
            # get coursenum and term from POST
            term = request.form.get("term")
            coursenum = request.form.get("coursenum")

            # check if the choosen course exists
            cur = con.execute("SELECT * FROM courses Where term = '{}' and courseNum = '{}'".format(term,coursenum))
            rv = cur.fetchall()
            if(not rv):
                flash(Markup("<font color=\"red\">Error: Course '{} {}' doesn't exist</font>".format(term, coursenum)),"error")
                return render_template("ta_manager.html")
            else:
                #return render_template("performance_log.html",term=term,coursenum=coursenum)
                return redirect(url_for('.perfor_log',term=term,coursenum=coursenum))
    return render_template("ta_manager.html")

@bp.route('/<term>/<coursenum>/perfor_log', methods=["GET","POST"])
def perfor_log(term,coursenum):
    # get database connection
    con = db.get_db()
    cur = con.execute("SELECT * FROM tacohort WHERE term = '{}' AND coursesapplied LIKE '%{}%'".format(term,coursenum))
    rv = cur.fetchall()
    for ta in rv:
        flash(Markup("<a href=\"?tid={}\">{}</a>".format(ta['tid'],ta['tname'])),"ta")
    
    tid = request.args.get('tid')
    tname = ""
    
    #if(request.method == "GET"):
    if not tid is None:
        # find the tname with tid
        cur1 = con.execute("SELECT tname FROM tacohort WHERE tid={}".format(tid))
        rv1 = cur1.fetchall()
        tname=rv1[0]["tname"]
        
        func = request.form.get("submit")
        if func == "Submit":
            print("here")
            comments = request.form.get("talog")
            
            if comments == "":
                flash(Markup("<font color=\"red\">Error: Comments cannot be empty</font>"),"error")
                return render_template("performance_log.html",term=term,coursenum=coursenum,tname=tname)

            query = '''INSERT INTO talog
            (term, coursenum, tid, tname, comments) values
            ('{}','{}',{},'{}','{}')'''.format(term,coursenum,tid,tname,comments)

            try:
                con.execute(query)
                con.commit()
                flash(Markup("<i>Submit successfully!</i>"),"error")
            except Exception as e:
                print(str(e))

        return render_template("performance_log.html",term=term,coursenum=coursenum,tname=tname)
    else:
        func = request.form.get("submit")
        if func == "Submit":
            flash(Markup("<font color=\"red\">Error: Please select a TA</font>".format(term, coursenum)),"error")

    return render_template("performance_log.html",term=term,coursenum=coursenum)

@bp.route('/<term>/<coursenum>/wish_list', methods=["GET","POST"])
def wish_list(term,coursenum):
    # get database connection
    con = db.get_db()
    cur = con.execute("SELECT * FROM tacohort WHERE term = '{}' AND coursesapplied LIKE '%{}%'".format(term,coursenum))
    rv = cur.fetchall()
    for ta in rv:
        flash(Markup("<a href=\"?tid={}\">{}</a>".format(ta['tid'],ta['tname'])),"ta")
    
    tid = request.args.get('tid')
    tname = ""
    
    #if(request.method == "GET"):
    if not tid is None:
         # find the tname with tid
        cur1 = con.execute("SELECT tname FROM tacohort WHERE tid={}".format(tid))
        rv1 = cur1.fetchall()
        tname=rv1[0]["tname"]
        
        func = request.form.get("submit")
        if func == "Submit":
            print("here")
            comments = request.form.get("talog")
            
            # # get prof from courses table by using term and course
            # cur2 = con.execute("SELECT * FROM courses WHERE term = '{}' AND coursenum = '{}'".format(term,coursenum))
            # rv2 = cur2.fetchall()
            # pname = rv2[0]['instructor']

            # check if TA is already added
            cur3 = con.execute("SELECT * FROM wishlist WHERE tid = {}".format(tid))
            rv3 = cur3.fetchall()
            if(rv3):
                flash(Markup("<font color=\"red\">Error: TA {} is already added into wish-list</font>".format(tname)),"error")
                return render_template("wish_list.html",term=term,coursenum=coursenum,tname=tname)


            query = '''INSERT INTO wishlist
            (term, coursenum, tname, tid) values
            ('{}','{}','{}',{})'''.format(term,coursenum,tname,tid)

            try:
                con.execute(query)
                con.commit()
                flash(Markup("<i>Submit successfully!</i>"),"error")
            except Exception as e:
                print(str(e))

        return render_template("wish_list.html",term=term,coursenum=coursenum,tname=tname)
    else:
        func = request.form.get("submit")
        if func == "Submit":
            flash(Markup("<font color=\"red\">Error: Please select a TA</font>".format(term, coursenum)),"error")

    return render_template("wish_list.html",term=term,coursenum=coursenum)