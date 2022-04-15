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

create table studenttarating
(
    ratingId  int
        constraint studenttarating_pk
            primary key,
    Score     int,
    comments  varchar(500),
    term      varchar(10),
    coursenum varchar(10),
    tid       varchar(10),
    foreign key (term, coursenum, tid) references taassignment
);

create table talog
(
    logid     int
        constraint talog_pk
            primary key,
    term      varchar(10),
    coursenum varchar(10),
    tid       varchar(10),
    tname     varchar(30)
        constraint talog_tacohort_tname_fk
            references tacohort (tname),
    comments  Varchar(500),
    datetime  datetime,
    foreign key (term, coursenum, tid) references taassignment
);

create table wishlist
(
    wlid      int
        constraint wishlist_pk
            primary key,
    term      varchar(10),
    coursenum varchar(10)
        constraint wishlist_courses_coursenum_fk
            references courses (coursenum),
    tname     varchar(30),
    tid       varchar(10),
    constraint wishlist_tacohort_tid_tname_term_fk
        foreign key (tid, tname, term) references tacohort (tid, tname, term)
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

create table taapplication
(
    jobapp            varchar(30),
    studentid         varchar(10)
        constraint taapplication_pk
            primary key,
    legalname         varchar(30),
    degreeyear        varchar(20),
    preferences       varchar(30),
    previous          varchar(20),
    legalworker       boolean,
    country           varchar(20),
    email             varchar(50),
    dateapplied       date,
    location          varchar(20),
    phone             varchar(20),
    field             varchar(30),
    numcoursesapplied int,
    lastcourse        varchar(10),
    course1           varchar(10),
    course1unit       integer,
    course2           varchar(10),
    course2unit       int,
    totalunits        int,
    assignment        varchar(30),
    recnotes          varchar(50),
    notes             varchar(100),
    coursesapplied    varchar(50),
    supervisor        varchar(20),
    priority          boolean,
    hrs180            boolean,
    mcgillemail       varchar(50),
    expsummary        VARCHAR(100),
    status            VARCHAR(20),
    diff              boolean,
    appin             varchar(20),
    flexible          boolean,
    previousworker    boolean
);

create table tahistory
(
    idlu       varchar(10)
        constraint tahistory_pk
            primary key,
    term       Varchar(10),
    coursenum  varchar(10),
    units      int,
    tname      varchar(30),
    degree     varchar(30),
    supervisor varchar(30),
    id         varchar(10),
    email      varchar(50),
    feedback   varchar(100)
);
