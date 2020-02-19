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
    return render_template("index.html")

@app.route("/test/add", methods=["POST"])
def add_test():
    data = xmltodict.parse(request.data)
    parsed = json.dumps(data)[0]

    with open("tsetfile", "w") as outfile:
        outfile.write(parsed)

    # naam opzoeken
    username = parsed["Catch"]["@name"]
    url = "http://localhost:82/user/%s" % username
    data = jsonify(requests.get(url=url))
    name = data[0][0]

    # lijst maken
    results = []
    for test_case in parsed["Catch"]["Group"]["TestCase"]:
        results.append((test_case["@name"], test_case["@filename"], test_case["OverallResult"]))
    results = str(jsonify(results)).replace('"', '\\"')

    # percentage berekenen
    failed = parsed["Catch"]["Group"]["OverallResults"]["@failures"]
    success = parsed["Catch"]["Group"]["OverallResults"]["@successes"]
    percent = int(success / (success + failed))

    # insert into db
    cursor = mysql.connection.cursor()
    cursor.execute("insert into student (name, data, percent) values (%s, %s, %s) on duplicate key update data=values(data), percent=values(percent);", (name, results, percent))
    mysql.connection.commit()
    cursor.close()

    return "success"

@app.route("/student/<username>")
def detail(username):
    # naam ophalen uit andere flask backend op :80 + database call voor alle tests op te halen
    name = "Stijn Taelemans"
    return render_template("detail.html", data=(name))

@app.route("/hook", methods=["POST"])
def hook():
    #dingen doen met request.data
    #code clonen
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

    # dingen doen met de output -> omzetten naar juiste / foute tests en doorgeven aan view

    #pagina updaten
    return "success"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True)
