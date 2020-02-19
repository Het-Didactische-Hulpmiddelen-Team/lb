import os, subprocess, git, xmltodict, requests
from flask import Flask, render_template, request, jsonify, json
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'dht'
app.config['MYSQL_PASSWORD'] = 'mvghetdhtmvghetdht'
app.config['MYSQL_DB'] = 'dht'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

@app.route("/")
def index():
    # compleet overzicht van alle studenten met hun percentage geslaagde tests
    # haalt de naam

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name, percent FROM student order by name")
    users = cursor.fetchall()
    cursor.close()
    return render_template("index.html", users=users)

@app.route("/test/add", methods=["POST"])
def add_test():
    # deze endpoint wordt opgeroepen door het run_tests script en voegt de huidige status
    # van de tests van een student toe aan de databank

    data = xmltodict.parse(request.data)
    parsed = json.dumps(data)[0]

    # naam opzoeken
    username = parsed[0][0]
    name = ""
    url = "http://localhost:82/user/%s" % username
    rq = requests.get(url=url)
    if rq.text != "[]":
        data = json.loads(rq.text)
        name = data[0][0]
    else:
        name = username

    # lijst maken
    results = []
    for test_case in parsed[0][1][2]:
        results.append((test_case[2], test_case[0], test_case[3][0]))
    results = str(jsonify(results)).replace('"', '\\"')

    # percentage berekenen
    failed = parsed[0][1][1][1]
    success = parsed[0][1][1][2]
    percent = int(success / (success + failed))

    # insert into db
    cursor = mysql.connection.cursor()
    cursor.execute("insert into student (name, data, percent) values (%s, %s, %s) on duplicate key update data=values(data), percent=values(percent);", (name, results, percent))
    mysql.connection.commit()
    cursor.close()

    return "success"

@app.route("/student/<username>")
def detail(username):
    # detailpagina die de status van elke test individueel laat zien

    name = "Stijn Taelemans"
    return render_template("detail.html", data=(name))

@app.route("/hook", methods=["POST"])
def hook():
    # wordt opgeroepen bij elke push in de organisatie
    # runt script dat c++ code compileert en test (zie ~/eindwerk/lb_repos/run_tests)

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
    os.chdir("/root/eindwerk/lb_repos")
    rc = subprocess.call(["run_tests", str(name)])
    print(rc)
    # teruggaan voor de zekerheid
    os.chdir("/root/eindwerk/lb")
    return "success"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True)
