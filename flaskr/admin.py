import os
from flask import Flask, Blueprint, render_template, request, url_for, flash, Markup, current_app
from email.message import EmailMessage
from . import db

bp = Blueprint("admin",__name__,url_prefix="/admin")

@bp.route('/info', methods=["GET","POST"]) 
def info():
    return render_template("info.html")

@bp.route('/update', methods=["GET","POST"]) 
def update():
    return render_template("update.html")

@bp.route('/adminimport', methods=["GET","POST"]) 
def adminimport():
    return render_template("adminimport.html")