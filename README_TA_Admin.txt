TODO for TA Admin:
1. test schema, load data once all done
2. add role
3. return to dashboard tbi

TA Administration Section (Orange): TA Info, Course TA Info, Update TA Info, Import (includes Bonus)
Navigate to different sections by clicking on the corresponding tab.

** TESTING **
** Please Import TACohort.csv and CourseQuota.csv Before Start Testing Using Sample Test Cases **
** Executing loaddata_ready_taadmin.sql has the same effect as importing required CSVs **

TA Info:
    User Input:
    1. Valid input:
        TA Student ID: ID matching a record in TACohort
    2. Invalid input:
        TA Student ID: ID with no matching record in TACohort

    Information Displayed:
    1. All data from TA Cohort
    2. Average student rating per course per term
    3. Student comments per course per term
    4. Professor Performance Log per course per term
    5. Professor Wishlist per course per term
    6. Courses Assigned per course per term

    Error Handling:
    1. Empty or invalid user input: Display error message

    Sample input for testing:
    1. 26000000: Successful case with all information
    2. 26000001: Successful case with partial information
    3. 26000010: Failure case due to no matching record.
    4. empty input: Failure case.

Course TA Info:
    User Input:
    1. Valid input:
        Term, Course Number: a pair of values matching a record in Courses
    2. Invalid input:
        Term, Course Number: a pair of values with no matching record in Courses

    Information Displayed:
    1. Student ID and name for each TA
    2. TA Quota for the course
    3. Current Number of TAs for the course
    4. Filled Rate (Current Number of TAs/TA Quota) for the course

    Error Handling:
    1. Empty or invalid user input: Display error message

    Sample input for testing:
    1. Winter2022, COMP307: Successful case with all information
    2. Winter2022, COMP421: Successful case with partial information
    3. Winter2022, COMP308: Failure case due to no matching record.
    4. empty input: Failure case.

Update TA Info:
    User Input:
    1. Valid input:
        Search: 
            Term, Course Number: values with matching a record
        Add:
            Term, Course Number, TA Student ID: TA and the course both exist in the given term
        Remove:
            Term, Course Number, TA Student ID: there exists an assignment of the TA to the course in the given term
        Update Hours:
            Term, TA Student ID, Hours: there exists an assignment of the TA to the course in the given term
        Update Name:
        Update Term:
        Update ID:
    2. Invalid input:
        Term, Course Number: a pair of values with no matching record in Courses

    Information Displayed:
    1. All relevant data for all TAs assigned for the course in the given term
    2. Feedback (Success messages) for actions (add TA, remove TA, update TA hours)

    Error Handling:
    1. Empty or invalid user input: Display error message

    Sample input for testing:
    1. Search: same as Course Info
    2. Add: 
        a. Winter2022, COMP307, 260000003: Successful case.
        b. Winter2022, COMP308, 260000003: Failure case due to no matching Course record.
        c. Winter2022, COMP307, 260000010: Failure case due to no matching TA record.
        d. Winter2022, COMP307, 260000003: Failure case due to assigning a TA to a course in a given term multiple times.
    3. Remove:
        a. Winter2022, COMP307, 260000003: Successful case.
        b. Winter2022, COMP308, 260000003: Failure case due to no matching TA Assignment record.
    4. Update Hours:
        a. Winter2022, 260000000, 180: Successful case.
        b. Winter2022, 260000010, 180: Failure case due to no matching TA record.
    5. Update Name:
        a. Winter2022, 260000000, Youyou: Successful case.
        b. Winter2022, 260000010, 180: Failure case due to no matching TA record.
    6. Update Term:
        a. 260000000, Winter2022, Winter2020: Successful case.
        b. 260000000, Winter2022, Winter2021: Failure case due to conflicting TA record.
        c. 260000010, Winter2022, Winter2021: Failure case due to no matching TA record.
    7. Update TA Student ID:
        a. Winter2022, 260000002, 260000011: Successful case.
        b. Winter2022, 260000000, 260000001: Failure case due to conflicting TA record.
        c. Winter2022, 260000010, 260000011: Failure case due to no matching TA record.
    8. empty input: Failure case.

Import:
User Input:
    1. Valid input:
        CSV files matching the description
    2. Invalid input:
        a. file extension is not .csv
        b. fields in files are not as expected

    Information Displayed:
    1. Feedback message for import.

    Error Handling:
    1. Empty or invalid user input: Display error message

    Sample input for testing: Plese use testdata csv files provided in data. 
    1. testdata_CourseQuota.csv
    2. testdata_TACohort.csv
    3. testdata_bonus_ugrad.csv
    4. testdata_grad.csv
    5. testdata_history.csv

N.B: There has been modifications on specific error handling and messages since the recording of the demo.
