import db
from flask import render_template, g, redirect, url_for, request, flash

def selectCourse():
    if not g.user:
        return redirect(url_for('dashboard'))

    connection = db.get_db()
    cursor = connection.execute('SELECT c.coursenum, c.coursename, c.term FROM registeredTable AS r, courses AS c WHERE r.studentId={} AND r.coursenum = c.coursenum'.format(g.user.studentId))
    courselist = cursor.fetchall()
    cursor.close()

    

    if request.method == 'POST':
        ta = request.form.get('submit_button')
        if ta == None:
            courseInfo =  request.form.get('course').split(",")
            cnum = courseInfo[0]
            term = courseInfo[1]
            cur1 = connection.execute("SELECT tid from taassignment WHERE coursenum = '{}' AND term = '{}'".format(cnum, term))
            tidlist = cur1.fetchall()
            cur1.close()
            infolist = []
            for tid in tidlist:
                cur2 = connection.execute("SELECT firstname, lastname, studentId FROM users where studentId = {};".format(tid[0]))
                result = cur2.fetchone()
                infolist.append(result)
            cur2.close()
            
            return render_template("TAlist.html", courseInfo = courseInfo, infolist = infolist)
        else:
            score = request.form.get('score')
            comment = request.form.get('comment')
            info = request.form.get('submit_button').split(',')
            cnum = info[0]
            term = info[1]
            tid = info[2]
            connection = db.get_db()
            query = "INSERT INTO studenttarating (Score, comments, term, coursenum, tid) VALUES ({}, '{}', '{}', '{}', {})".format(score, comment, term, cnum,tid)
            cur = connection.execute(query)
            connection.commit()
            cur.close()

            cur1 = connection.execute("SELECT tid from taassignment WHERE coursenum = '{}' AND term = '{}'".format(cnum, term))
            tidlist = cur1.fetchall()
            cur1.close()
            infolist = []
            for tid in tidlist:
                cur2 = connection.execute("SELECT firstname, lastname, studentId FROM users where studentId = {};".format(tid[0]))
                result = cur2.fetchone()
                infolist.append(result)
            flash("The rating is submitted. Thank you for your feedback.")
            return render_template("TAlist.html", courseInfo = info, infolist = infolist)
    return render_template("selectCourse.html", courselist=courselist)
selectCourse.methods=["GET", "POST"]
'''
def rate():
    courseInfo = request.args['cnum']
    infolist = request.args['term']
    return render_template("TAlist.html", courseInfo=courseInfo, infolist=infolist)
rate.methods=["GET", "POST"]
'''