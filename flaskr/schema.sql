DROP TABLE IF EXISTS userAccounts;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS registeredTable;

CREATE TABLE userAccounts (
    username VARCHAR(20) PRIMARY KEY,
    userpassword VARCHAR(20) NOT NULL,
    useremail VARCHAR(50),
    isStudent BOOLEAN,
    isProf BOOLEAN,
    isSysop BOOLEAN,
    isAdmin BOOLEAN,
    isTA BOOLEAN     
);

CREATE TABLE courses (
    courseNum VARCHAR(10) PRIMARY KEY,
    term VARCHAR(20) NOT NULL,
    courseName VARCHAR(50) NOT NULL,
    instructor VARCHAR(50) NOT NULL
);

CREATE TABLE users(
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname VARCHAR(40) NOT NULL,
    lastname VARCHAR(40) NOT NULL,
    studentId INTEGER,
    username VARCHAR(20),
    FOREIGN KEY(username) REFERENCES userAccounts(username)
);

CREATE TABLE registeredTable(
    userid INTEGER,
    courseNum VARCHAR(10),
    PRIMARY KEY (userid,courseNum),
    FOREIGN KEY(userid) REFERENCES users(userid),
    FOREIGN KEY(courseNum) REFERENCES courses(courseNum)
);

