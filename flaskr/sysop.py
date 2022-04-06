from flaskr import app
from database import get_db
import pandas
import smtplib, ssl
from email.message import EmailMessage

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
        db = get_db()
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