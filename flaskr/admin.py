import json
import os
import sqlite3
from xmlrpc.client import TRANSPORT_ERROR
from flask import Flask, Blueprint, render_template, request, url_for, flash, Markup, current_app
from email.message import EmailMessage

from sklearn.utils import resample
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

@bp.route('/adminimport', methods=["GET","POST"]) 
def adminimport():
    return render_template("adminimport.html")