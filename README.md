# LeaderBoard - LB

# Usage
Before setting up this webserver make sure you have these pip packages installed:
* requests
* gitpython
* flask
* flask_mysqldb

## Database
You can change the database used in lines 9 - 13.

# Routes
* "/" : Shows the index.html page which includes a list of the progress of all students
* "/test/add" : This route should only be used by the script that is ran server-side. You are not supposed to send any POST or GET request to this route.
* "/student/-username-" : Surfing to this route will show the user the individual progress for a student. A more in depth look in which tests are failing is given here.
* "/hook" : Don't use this route, this is intended for requests comming from Github.

# Additional setup
- On line 44 a url is specified that points to the GTN service (more info on this can be found in our 'gtn' project). You can either point it to your own webapp running the GTN software or remove lines 44 - 49 all together.
- On line 142 a path variable is declared which you can change to fit your needs. This is where the students' repos will be clones to. We strongly advise you to not change this to eliminate potential errors in the script that runs the tests for the repos.
- If you didn't change the path in the previous step you should make sure there is a folder in the filesystem on that location ('../lb_repos/')
- On line 150 a path to the script that runs the tests is specified.

