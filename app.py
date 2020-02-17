import os

from flask import Flask, render_template, request, jsonify, json
from pip._internal.vcs import git

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
    path = "repos/" + json.loads(data)["repository"]["full_name"]

    if os.path.exists(path):
        # pull
        git.Git(path).pull(url)
    else:
        # clone
        os.makedirs(path)
        git.Git(path).clone(url)

    #tests rerunnen

    #pagina updaten
    return "success"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True)