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

create table courses
(
    term       VARCHAR(20) not null,
    coursenum  VARCHAR(10) not null,
    coursetype VARCHAR(20) not null,
    coursename VARCHAR(50) not null,
    instructor VARCHAR(50) not null,
    enrollnum  integer default '0',
    taquota    integer,
    constraint courses_pk
        primary key (term, coursenum)
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

create table tacohort
(
    term           VARCHAR(10),
    tname          varchar(30),
    tid            VARCHAR(20),
    legalname      varchar(50),
    email          varchar(30),
    ugrad          boolean,
    supervisor     varchar(30),
    priority       boolean default false,
    hours          integer,
    applieddate    date,
    location       varchar(20),
    phone          VArchar(20),
    degree         varchar(30),
    coursesapplied Varchar(50),
    flexible       boolean,
    notes          varchar(100),
    constraint tacohort_pk
        primary key (term, tid)
);

create table taassignment
(
    term      VARchar(10) not null,
    coursenum varchar(10) not null,
    tid       varchar(10) not null
        references tacohort (tid)
            on update restrict,
    active    boolean     not null,
    constraint taassignment_pk
        primary key (term, coursenum, tid),
    foreign key (term, coursenum) references courses
        on update restrict
);

