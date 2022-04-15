-- load data before testing TA Administration (Orange Section)
-- courses
INSERT INTO courses (term, coursenum, coursetype, coursename, instructor, enrollnum, taquota) VALUES ('Winter2021', 'COMP421', 'Science', 'Database', 'Joseph D', 400, 20);
INSERT INTO courses (term, coursenum, coursetype, coursename, instructor, enrollnum, taquota) VALUES ('Winter2021', 'COMP307', 'Science', 'Web Dev', 'Joseph V', 100, 5);

-- tacohort
INSERT INTO tacohort (term, tname, tid, legalname, email, ugrad, supervisor, priority, hours, applieddate, location, phone, degree, coursesapplied, flexible, notes) VALUES ('Winter2022', 'Claire', '260000000', 'Youyou Yang', 'youyou.yang@mail.mcgill.ca', 1, 'Joseph V', 1, 90, '2021-12-01', 'Canada', '5140000000', 'Bachelor of Science', 'COMP307', 1, 'good');
INSERT INTO tacohort (term, tname, tid, legalname, email, ugrad, supervisor, priority, hours, applieddate, location, phone, degree, coursesapplied, flexible, notes) VALUES ('Winter2022', 'Alice', '260000001', 'Alice Pan', 'alice.pan@mail.mcgill.ca', 1, 'Joseph V', null, 180, '2021-12-01', 'Canada', '5140000001', 'Bachelor of Science', 'COMP307, COMP421', 1, 'very good');
INSERT INTO tacohort (term, tname, tid, legalname, email, ugrad, supervisor, priority, hours, applieddate, location, phone, degree, coursesapplied, flexible, notes) VALUES ('Winter2022', 'Ruby', '260000002', 'Ruaby', 'ruaby@mail.mcgill.ca', 1, 'Joseph V', 1, 90, '2021-12-01', 'Canada', '5150000002', 'Bachelor of Science', 'COMP307, CHEM181', 1, 'great');
INSERT INTO tacohort (term, tname, tid, legalname, email, ugrad, supervisor, priority, hours, applieddate, location, phone, degree, coursesapplied, flexible, notes) VALUES ('Winter2022', 'Xingyi', '260000003', 'Xingyi Wang', 'xingyi.wang@mail.mcgill.ca', 1, 'Joseph V', 1, 90, '2021-12-01', 'Canada', '5140000003', 'Bachelor of Science', 'COMP307', 1, 'very very good');
INSERT INTO tacohort (term, tname, tid, legalname, email, ugrad, supervisor, priority, hours, applieddate, location, phone, degree, coursesapplied, flexible, notes) VALUES ('Winter2022', 'Qiqi', '260000004', 'Qiqi Su', 'qq.s@mail.mcgill.ca', 1, 'Joseph V', 1, 90, '2021-12-01', 'Canada', '5140000004', 'Bachelor of Science', 'COMP307', 0, null);

-- taassignmnet
INSERT INTO taassignment (term, coursenum, tid, active) VALUES ('Winter2022', 'COMP307', '260000000', 1);
INSERT INTO taassignment (term, coursenum, tid, active) VALUES ('Winter2022', 'COMP307', '260000001', 1);
INSERT INTO taassignment (term, coursenum, tid, active) VALUES ('Winter2021', 'COMP307', '260000000', 1);
INSERT INTO taassignment (term, coursenum, tid, active) VALUES ('Winter2022', 'COMP307', '260000002', 1);

-- taassignmnet
INSERT INTO taassignment (term, coursenum, tid, active) VALUES ('Winter2022', 'COMP307', '260000000', 1);
INSERT INTO taassignment (term, coursenum, tid, active) VALUES ('Winter2022', 'COMP307', '260000001', 1);
INSERT INTO taassignment (term, coursenum, tid, active) VALUES ('Winter2021', 'COMP307', '260000000', 1);
INSERT INTO taassignment (term, coursenum, tid, active) VALUES ('Winter2022', 'COMP307', '260000002', 1);

-- talog
INSERT INTO talog (logid, term, coursenum, tid, tname, comments, datetime) VALUES (1, 'Winter2022', 'COMP307', '260000000', 'Claire', 'Responsible TA.', null);
INSERT INTO talog (logid, term, coursenum, tid, tname, comments, datetime) VALUES (2, 'Winter2022', 'COMP307', '260000000', 'Claire', 'Very responsible TA.', null);

-- studenttarating
INSERT INTO studenttarating (ratingId, Score, comments, term, coursenum, tid) VALUES (1, 1, 'Bad TA.', 'Winter2022', 'COMP307', '260000000');
INSERT INTO studenttarating (ratingId, Score, comments, term, coursenum, tid) VALUES (2, 2, 'Okay TA.', 'Winter2022', 'COMP307', '260000000');
INSERT INTO studenttarating (ratingId, Score, comments, term, coursenum, tid) VALUES (3, 3, 'Good TA.', 'Winter2022', 'COMP307', '260000000');
INSERT INTO studenttarating (ratingId, Score, comments, term, coursenum, tid) VALUES (4, 4, 'Very good.', 'Winter2021', 'COMP307', '260000000');

-- wishlist
INSERT INTO wishlist (wlid, term, coursenum, tname, tid) VALUES (1, 'Winter2022', 'COMP307', 'Claire', '260000000');