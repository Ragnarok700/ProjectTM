"""
ProjectTM
app.py
Load webpages and handle routes
"""

import io
from flask import Flask, render_template, redirect, url_for, request
from controller import *
from tournament_5v5 import *
from summonerinfo import *

# Creates Flask Webapp Object
app = Flask(__name__)

# Riot Games API Key
api_key = utils.read_key()

# Home Page
@app.route("/")
def home():
    return render_template('index.html')

# Teams Display Page (Prospective)
@app.route("/teams")
def view_teams():
    pass

# Handles .csv file with player data to generate teams
@app.route("/", methods=['POST'])
def upload_file():
    # Getting .csv file from request object
    uploaded_file = request.files['file']
    # Check whether the file exists or not
    if uploaded_file.filename == '':
        return redirect(url_for("home"))
    # Converts the content of the file to text
    stream = io.StringIO(request.files['file'].stream.read().decode("UTF8"), newline=None)

    # Call the function in the Controller to read the player data and return a list of players
    players = read_player_data(stream)

    print("\n##### CREATING TEAMS #####\n")
    # Generates a dictionary of balanced teams
    teams = create_tournament_5v5(players, [GameMode.NORMAL, GameMode.RANKED])

    # IGNORE : USED FOR DEBUGGING
    # Displays the content in the console
    i = 1
    for team in teams.values():
        print(f"\n### TEAM #{i} ###\n")
        i += 1
        for player in team:
            print(player)
    #####

    # Builds a string to represent a web page for displaying the teams
    i = 1
    bad_implementation = ""
    for team in teams.values():
        bad_implementation += f"<br/><br/>### TEAM #{i} ###<br/><br>"
        i += 1
        for player in team:
            bad_implementation += f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{player.getName()} --- "{player.getDiscord()}" --- "{player.getSummoner().getName()}" --- {player.getAssignedRole().name}<br/>'
    return bad_implementation

if __name__ == "__main__":
    app.run()