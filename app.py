import os, subprocess, git, requests, re,sys
import xml.etree.ElementTree as et
from flask import Flask, render_template, request, jsonify, json
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_USER'] = 'dht'
app.config['MYSQL_PASSWORD'] = 'mvghetdhtmvghetdht'
app.config['MYSQL_DB'] = 'lb'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

@app.route("/")
def index():
    # compleet overzicht van alle studenten met hun percentage geslaagde tests
    # haalt de naam

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name, assertions, testcases, testfiles FROM student order by name")
    users = cursor.fetchall()
    cursor.close()
    totalassertions = getTotalAssertions()
    totalcases = getTotalTestCases()
    totalfiles = getTotalTestFiles()
    users2 = []
    for i,stud in enumerate(users):
        name = users[i][0]
        assertionsperc = int(int(users[i][1]) / totalassertions * 100)
        caseperc = int(int(users[i][2]) / totalcases * 100)
        filesperc = int(int(users[i][3]) / totalfiles * 100)
        users2.append([name, assertionsperc, caseperc, filesperc])
    return render_template("index.html", users=users2)

@app.route("/test/add", methods=["POST"])
def add_test():
    # deze endpoint wordt opgeroepen door het run_tests script en voegt de huidige status
    # van de tests van een student toe aan de databank
    # https://docs.python.org/2/library/xml.etree.elementtree.html
    root = et.fromstring(request.data)
    group = root.find("Group")

    # naam opzoeken
    username = group.attrib["name"]
    name = username
    url = "http://localhost:82/user/%s" % username
    rq = requests.get(url=url)
    if rq.text != "[]":
        data = json.loads(rq.text)
        name = data[0][0]

    # json maken van alle testcases, alleen nodige data overhouden
    results = {}
    cases = 0
    for i, testcase in enumerate(group):
        dic = {}
        if testcase.tag == "TestCase":
            dic["name"] = testcase.attrib["name"].replace('"', '\\"').replace("'", "\\'")
            dic["filename"] = testcase.attrib["filename"]
            dic["result"] = testcase.find("OverallResult").attrib["success"]
            cases += 1
        results[i] = dic
    results = json.dumps(results)

    overall_results = root.find("OverallResults")
    success = int(overall_results.attrib["successes"])
    failed = int(overall_results.attrib["failures"])
    files = int(overall_results.attrib["compiledFiles"])

    # insert into db
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO student(name, data, assertions, testcases, testfiles) values (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE data=values(data), assertions=values(assertions), testcases=values(testcases), testfiles=values(testfiles);", (name, results, success, cases, files))
    mysql.connection.commit()
    cursor.close()

    return "success"

def getTotal(param):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT "+param+" FROM student WHERE name=\'Fréderik Vogels\';")
    res = cursor.fetchall()
    cursor.close()
    return res[0][0]
def getTotalAssertions():
    return getTotal("assertions")
def getTotalTestCases():
    return getTotal("testcases")
def getTotalTestFiles():
    return getTotal("testfiles")

@app.route("/student/<username>")
def detail(username):
    # detailpagina die de status van elke test individueel laat zien
    name = re.sub("%20", " ", username)

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM student WHERE name=\'"+name+"\';")
    res = cursor.fetchall()
    cursor.close()

    percent = res[0][2]
    tests = json.loads(res[0][1])
    vals = tests.values()
    
    files = []
    for i, x in enumerate(vals):
        if i != len(vals) - 1:
            files.append(re.sub('./tests/', "", x["filename"]) )
    files.sort()
    
    def build_nested_helper(path, text, container):
        segs = path.split('/')
        head = segs[0]
        tail = segs[1:]
        if not tail:
            container[head] = text
        else:
            if head not in container:
                container[head] = {}
            build_nested_helper('/'.join(tail), tail[0], container[head])

    def build_nested(paths):
        container = {}
        for path in paths:
            build_nested_helper(path, path, container)
        return container
    d = build_nested(files)
    
    return render_template("detail.html", name=name, ul=d, percent=percent)

@app.route("/hook", methods=["POST"])
def hook():
    # wordt opgeroepen bij elke push in de organisatie
    # runt script dat c++ code compileert en test (zie /root/eindwerk/lb_repos/run_tests)

    # code clonen
    data = request.data
    url = json.loads(data)["repository"]["url"]
    name = json.loads(data)["repository"]["name"]
    path = "../lb_repos/"

    if os.path.exists(path+name):
        git.Git(path+name).pull(url)
    else:
        git.Git(path).clone(url)

    #tests rerunnen
    rc = subprocess.call(["/root/eindwerk/lb_repos/run_tests", str(name)])
    return "success"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True)
