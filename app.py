import os
import subprocess
import git
from flask import Flask, render_template, request, jsonify, json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

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
    rc = subprocess.call([path+"run_tests", str(name)])
    print(rc)

    # dingen doen met de output -> omzetten naar juiste / foute tests en doorgeven aan view

    #pagina updaten
    return "success"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True)
