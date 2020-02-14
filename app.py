from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/student/<username>")
def detail():
    return render_template("detail.html")

@app.route("/hook", methods=["POST"])
def hook():
    #dingen doen met request.data
    #code clonen
    #tests rerunnen
    #pagina updaten
    return "success"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)