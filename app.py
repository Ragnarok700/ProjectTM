# William Tom
# 4/13/21
import io
import utils
from flask import Flask, render_template, redirect, url_for, request
from controller import *
from tournament_5v5 import *
from summonerinfo import *

app = Flask(__name__)

api_key = utils.read_key()

# Home Page
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/<name>")
def user (name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin!"))

@app.route("/teams")
def view_teams():
    pass

@app.route("/", methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return redirect(url_for("home"))
    stream = io.StringIO(request.files['file'].stream.read().decode("UTF8"), newline=None)

    players = read_player_data(stream)

    print("\n##### CREATING TEAMS #####\n")
    teams = tournament_5v5.tournament_5v5(players, [GameMode.NORMAL, GameMode.RANKED])
    i = 1
    for team in teams:
        print(f"### TEAM #{i} ###")
        for player in team:
            print(player)

    return redirect(url_for("home"))
    #return redirect(url_for("user", name="Admin!"))

if __name__ == "__main__":
    app.run()