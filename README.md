# LeaderBoard - LB

# Usage
Before setting up this webserver make sure you have these pip packages installed:
* requests
* gitpython
* flask
* flask_mysqldb

# Database
You can change the database used in lines 9 - 13in app.py.

This is the MySQL syntax to setup the tables needed:
```sql
CREATE DATABASE lb;
use lb;
CREATE TABLE student(
    name VARCHAR(50) PRIMARY KEY,
    data JSON,
    assertions INT,
    testcases INT,
    testfiles INT
)
```

# IMPORTANT
You are supposed to have a record in the DB that has info about the max amount of testcases/assertions present. This can be done in 2 ways:
- By using GTN: You will first have to 'link' your githubname to the name 'Frédéric Vogels' (changeable in code) before pushing a !finished! project to the organisation in a repo under your github account. The server will run tests and enter this record into the database
```
'Frédéric Vogels' | //some-json// | totalAssertions | totalTestCases | totalTestFiles
```
- By adding a record to the database with this MySQL syntax:
```sql
INSERT INTO student(name, data, assertions, testcases, testfiles) VALUES
('Frédéric Vogels', NULL, <totalAssertions>, <totalCases>, <totalTestFiles>);
```

# Routes
* "/" : Shows the index.html page which includes a list of the progress of all students
* "/test/add" : This route should only be used by the script that is ran server-side. You are not supposed to send any POST or GET request to this route.
* "/student/-username-" : Surfing to this route will show the user the individual progress for a student. A more in depth look in which tests are failing is given here.
* "/hook" : Don't use this route, this is intended for requests comming from Github.

# Additional setup
- On line 15 a url is specified that points to the GTN service (more info on this can be found in our 'gtn' project). You can either point it to your own webapp running the GTN software or remove lines 44 - 49 all together.
- On line 16 a path variable is declared which you can change to fit your needs. This is where the students' repos will be clones to. We strongly advise you to not change this to eliminate potential errors in the script that runs the actual tests for the repos.
- If you didn't change the path in the previous step you should make sure there is a folder in the filesystem on that location ('../lb_repos/')
- Into the folder created in the previous step you want to copy the 'run_tests' script
```
cp run_tests ../lb_repos/
```
- On line 17 a path to the script that runs the tests is specified. Change this to the correct folder.
- On line 18 can be found the variable to change the portnr the server runs on.

