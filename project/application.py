import os
import random

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, json, url_for, jsonify
from flask_session import Session
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///teams.db")









def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""

    rating1 = team1[1]
    rating2 = team2[1]
    probability = 10 / (1 + 10 ** ((rating2 - rating1) / 600))
    result = random.randrange(10)
    if result == round(probability):
        return 2
    else:
        return result < round(probability)

def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners

def simulate_group(teams):
    """Simulates a group. Returns a list of winners from each match."""
    winners = []
    i = 1
    # Simulates all games in a group
    for team in teams:
        rounds = 0
        while i < len(teams):
            result = simulate_game(team, teams[i])
            if result == 2:
                winners.append([team, teams[i]])
            elif result:
                winners.append(team)
            else:
                winners.append(teams[i])
            i += 1
            rounds += 1
        i -= rounds
        i += 1
    return winners

groupWinners=['','', '', '', '', '', '', '', '', '', '', '', '', '', '', '']




@app.route("/", methods=["GET", "POST"])
def index():
    """Home Page"""
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        if request.form.get("finals"):
            db.execute("DELETE FROM teams")
            db.execute("DELETE FROM groupA")
            db.execute("DELETE FROM groupB")
            db.execute("DELETE FROM groupC")
            db.execute("DELETE FROM groupD")
            db.execute("DELETE FROM groupE")
            db.execute("DELETE FROM groupF")
            db.execute("DELETE FROM groupG")
            db.execute("DELETE FROM groupH")
            finals = db.execute("SELECT * FROM finals")
            groupWinners=['','', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            for team in finals:
                db.execute("INSERT INTO teams(id, name, points, conference) VALUES (?, ?, ?, ?)", team["id"], team["name"], team["points"], team["conference"])
            return redirect("/finals")
        if request.form.get("qualifiers"):
            db.execute("UPDATE conmebol SET points = 0")
            db.execute("UPDATE concacaf SET points = 0")
            db.execute("UPDATE caf SET points = 0")
            db.execute("UPDATE afc SET points = 0")
            db.execute("UPDATE uefa SET points = 0")
            db.execute("DELETE FROM teams")
            db.execute("DELETE FROM playoff WHERE conference = ?", "AFC")
            db.execute("DELETE FROM playoff WHERE conference = ?", "CONMEBOL")
            db.execute("DELETE FROM playoff WHERE conference = ?", "CONCACAF")
            db.execute("DELETE FROM groupA")
            db.execute("DELETE FROM groupB")
            db.execute("DELETE FROM groupC")
            db.execute("DELETE FROM groupD")
            db.execute("DELETE FROM groupE")
            db.execute("DELETE FROM groupF")
            db.execute("DELETE FROM groupG")
            db.execute("DELETE FROM groupH")
            groupWinners=['','', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            return redirect("/conmebol")
        return redirect("/")

@app.route("/finals", methods=["GET", "POST"])
def finals():
    """World Cup Finals"""

    if request.method == "GET":
        # Gathers teams to be sorted into groups
        teams = db.execute("SELECT * FROM teams WHERE name <> 'Qatar' ORDER BY points DESC")
        host = db.execute("SELECT * FROM teams WHERE name = 'Qatar'")

        # Creates groups
        groupA = db.execute("SELECT * FROM groupA ORDER BY position")
        groupB = db.execute("SELECT * FROM groupB ORDER BY position")
        groupC = db.execute("SELECT * FROM groupC ORDER BY position")
        groupD = db.execute("SELECT * FROM groupD ORDER BY position")
        groupE = db.execute("SELECT * FROM groupE ORDER BY position")
        groupF = db.execute("SELECT * FROM groupF ORDER BY position")
        groupG = db.execute("SELECT * FROM groupG ORDER BY position")
        groupH = db.execute("SELECT * FROM groupH ORDER BY position")

        if not groupA:
            db.execute("INSERT INTO groupA (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[0]["id"], teams[0]["name"], 1, 0)
            db.execute("INSERT INTO groupA (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[8]["id"], teams[8]["name"], 2, 0)
            db.execute("INSERT INTO groupA (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[16]["id"], teams[16]["name"], 3, 0)
            db.execute("INSERT INTO groupA (teams_id, name, position, points) VALUES(?, ?, ?, ?)", host[0]["id"], host[0]["name"], 4, 0)

        if not groupB:
            db.execute("INSERT INTO groupB (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[1]["id"], teams[1]["name"], 1, 0)
            db.execute("INSERT INTO groupB (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[9]["id"], teams[9]["name"], 2, 0)
            db.execute("INSERT INTO groupB (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[17]["id"], teams[17]["name"], 3, 0)
            db.execute("INSERT INTO groupB (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[24]["id"], teams[24]["name"], 4, 0)

        if not groupC:
            db.execute("INSERT INTO groupC (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[2]["id"], teams[2]["name"], 1, 0)
            db.execute("INSERT INTO groupC (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[10]["id"], teams[10]["name"], 2, 0)
            db.execute("INSERT INTO groupC (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[18]["id"], teams[18]["name"], 3, 0)
            db.execute("INSERT INTO groupC (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[25]["id"], teams[25]["name"], 4, 0)

        if not groupD:
            db.execute("INSERT INTO groupD (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[3]["id"], teams[3]["name"], 1, 0)
            db.execute("INSERT INTO groupD (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[11]["id"], teams[11]["name"], 2, 0)
            db.execute("INSERT INTO groupD (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[19]["id"], teams[19]["name"], 3, 0)
            db.execute("INSERT INTO groupD (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[26]["id"], teams[26]["name"], 4, 0)

        if not groupE:
            db.execute("INSERT INTO groupE (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[4]["id"], teams[4]["name"], 1, 0)
            db.execute("INSERT INTO groupE (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[12]["id"], teams[12]["name"], 2, 0)
            db.execute("INSERT INTO groupE (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[20]["id"], teams[20]["name"], 3, 0)
            db.execute("INSERT INTO groupE (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[27]["id"], teams[27]["name"], 4, 0)

        if not groupF:
            db.execute("INSERT INTO groupF (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[5]["id"], teams[5]["name"], 1, 0)
            db.execute("INSERT INTO groupF (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[13]["id"], teams[13]["name"], 2, 0)
            db.execute("INSERT INTO groupF (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[21]["id"], teams[21]["name"], 3, 0)
            db.execute("INSERT INTO groupF (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[28]["id"], teams[28]["name"], 4, 0)

        if not groupG:
            db.execute("INSERT INTO groupG (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[6]["id"], teams[6]["name"], 1, 0)
            db.execute("INSERT INTO groupG (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[14]["id"], teams[14]["name"], 2, 0)
            db.execute("INSERT INTO groupG (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[22]["id"], teams[22]["name"], 3, 0)
            db.execute("INSERT INTO groupG (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[29]["id"], teams[29]["name"], 4, 0)

        if not groupH:
            db.execute("INSERT INTO groupH (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[7]["id"], teams[7]["name"], 1, 0)
            db.execute("INSERT INTO groupH (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[15]["id"], teams[15]["name"], 2, 0)
            db.execute("INSERT INTO groupH (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[23]["id"], teams[23]["name"], 3, 0)
            db.execute("INSERT INTO groupH (teams_id, name, position, points) VALUES(?, ?, ?, ?)", teams[30]["id"], teams[30]["name"], 4, 0)



        r16teams = json.dumps(groupWinners)

        return render_template("finals.html", a=groupA, b=groupB, c=groupC, d=groupD, e=groupE, f=groupF, g=groupG, h=groupH, groupWinners=groupWinners, r16teams=r16teams)

    if request.method == "POST":

        table = request.form.get("A")

        # Simulate Group A
        if table == "Simulate Group A":

            # resets group points to 0
            db.execute("UPDATE groupA SET points = 0")

            # Gathers groupA teams and their ratings
            groupA = db.execute("SELECT * FROM groupA ORDER BY position, points DESC")
            ratings = [[groupA[0]["name"], 0], [groupA[1]["name"], 0], [groupA[2]["name"], 0], [groupA[3]["name"], 0]]
            i = 0
            for team in groupA:
                rating = db.execute("SELECT name, points FROM teams WHERE id = ?", team["teams_id"])
                print(rating)
                ratings[i][1] = rating[0]["points"]
                i += 1

            # Simulates the Group
            winners = simulate_group(ratings)

            # Updates Group A with the teams points and new position
            for win in winners:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM groupA WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM groupA WHERE name = ?", win[1][0])
                    db.execute("UPDATE groupA SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE groupA SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM groupA WHERE name = ?", win[0])
                    db.execute("UPDATE groupA SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            teams = db.execute("SELECT * FROM groupA ORDER BY points DESC")
            position = 1
            for team in teams:
                db.execute("UPDATE groupA SET position = ? WHERE name = ?", position, team["name"])
                position += 1

            # Adds top two teams to groupWinners array
            for team in ratings:
                if team in groupWinners:
                    groupWinners.insert(groupWinners.index(team), "")
                    groupWinners.remove(team)
                if teams[0]["name"] == team[0]:
                    groupWinners.pop(0)
                    groupWinners.insert(0, team)
                if teams[1]["name"] == team[0]:
                    groupWinners.pop(13)
                    groupWinners.insert(13, team)

            return redirect("/finals")

        table = request.form.get("B")

        # Simulate Group B
        if table == "Simulate Group B":

            # resets group points to 0
            db.execute("UPDATE groupB SET points = 0")

            # Gathers groupB teams and their ratings
            groupB = db.execute("SELECT * FROM groupB ORDER BY position, points DESC")
            ratings = [[groupB[0]["name"], 0], [groupB[1]["name"], 0], [groupB[2]["name"], 0], [groupB[3]["name"], 0]]
            i = 0
            for team in groupB:
                rating = db.execute("SELECT name, points FROM teams WHERE id = ?", team["teams_id"])
                ratings[i][1] = rating[0]["points"]
                i += 1

            # Simulates the Group
            winners = simulate_group(ratings)

            # Updates Group B with the teams points and new position
            for win in winners:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM groupB WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM groupB WHERE name = ?", win[1][0])
                    db.execute("UPDATE groupB SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE groupB SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM groupB WHERE name = ?", win[0])
                    db.execute("UPDATE groupB SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            teams = db.execute("SELECT * FROM groupB ORDER BY points DESC")
            position = 1
            for team in teams:
                db.execute("UPDATE groupB SET position = ? WHERE name = ?", position, team["name"])
                position += 1

            # Adds top two teams to groupWinners array
            for team in ratings:
                if team in groupWinners:
                    groupWinners.insert(groupWinners.index(team), "")
                    groupWinners.remove(team)
                if teams[0]["name"] == team[0]:
                    groupWinners.pop(12)
                    groupWinners.insert(12, team)
                if teams[1]["name"] == team[0]:
                    groupWinners.pop(1)
                    groupWinners.insert(1, team)

            return redirect("/finals")

        # Simulate Group C
        table = request.form.get("C")

        if table == "Simulate Group C":

            # resets group points to 0
            db.execute("UPDATE groupC SET points = 0")

            # Gathers groupC teams and their ratings
            groupC = db.execute("SELECT * FROM groupC ORDER BY position, points DESC")
            ratings = [[groupC[0]["name"], 0], [groupC[1]["name"], 0], [groupC[2]["name"], 0], [groupC[3]["name"], 0]]
            i = 0
            for team in groupC:
                rating = db.execute("SELECT name, points FROM teams WHERE id = ?", team["teams_id"])
                ratings[i][1] = rating[0]["points"]
                i += 1

            # Simulates the Group
            winners = simulate_group(ratings)

            # Updates Group C with the teams points and new position
            for win in winners:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM groupC WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM groupC WHERE name = ?", win[1][0])
                    db.execute("UPDATE groupC SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE groupC SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM groupC WHERE name = ?", win[0])
                    db.execute("UPDATE groupC SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            teams = db.execute("SELECT * FROM groupC ORDER BY points DESC")
            position = 1
            for team in teams:
                db.execute("UPDATE groupC SET position = ? WHERE name = ?", position, team["name"])
                position += 1

            # Adds top two teams to groupWinners array
            for team in ratings:
                if team in groupWinners:
                    groupWinners.insert(groupWinners.index(team), "")
                    groupWinners.remove(team)
                if teams[0]["name"] == team[0]:
                    groupWinners.pop(2)
                    groupWinners.insert(2, team)
                if teams[1]["name"] == team[0]:
                    groupWinners.pop(15)
                    groupWinners.insert(15, team)

            return redirect("/finals")

        # Simulate Group D
        table = request.form.get("D")

        if table == "Simulate Group D":

            # resets group points to 0
            db.execute("UPDATE groupD SET points = 0")

            # Gathers groupD teams and their ratings
            groupD = db.execute("SELECT * FROM groupD ORDER BY position, points DESC")
            ratings = [[groupD[0]["name"], 0], [groupD[1]["name"], 0], [groupD[2]["name"], 0], [groupD[3]["name"], 0]]
            i = 0
            for team in groupD:
                rating = db.execute("SELECT name, points FROM teams WHERE id = ?", team["teams_id"])
                ratings[i][1] = rating[0]["points"]
                i += 1

            # Simulates the Group
            winners = simulate_group(ratings)

            # Updates Group D with the teams points and new position
            for win in winners:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM groupD WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM groupD WHERE name = ?", win[1][0])
                    db.execute("UPDATE groupD SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE groupD SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM groupD WHERE name = ?", win[0])
                    db.execute("UPDATE groupD SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            teams = db.execute("SELECT * FROM groupD ORDER BY points DESC")
            position = 1
            for team in teams:
                db.execute("UPDATE groupD SET position = ? WHERE name = ?", position, team["name"])
                position += 1

            # Adds top two teams to groupWinners array
            for team in ratings:
                if team in groupWinners:
                    groupWinners.insert(groupWinners.index(team), "")
                    groupWinners.remove(team)
                if teams[0]["name"] == team[0]:
                    groupWinners.pop(14)
                    groupWinners.insert(14, team)
                if teams[1]["name"] == team[0]:
                    groupWinners.pop(3)
                    groupWinners.insert(3, team)

            return redirect("/finals")

        # Simulate Group E
        table = request.form.get("E")

        if table == "Simulate Group E":

            # resets group points to 0
            db.execute("UPDATE groupE SET points = 0")

            # Gathers groupE teams and their ratings
            groupE = db.execute("SELECT * FROM groupE ORDER BY position, points DESC")
            ratings = [[groupE[0]["name"], 0], [groupE[1]["name"], 0], [groupE[2]["name"], 0], [groupE[3]["name"], 0]]
            i = 0
            for team in groupE:
                rating = db.execute("SELECT name, points FROM teams WHERE id = ?", team["teams_id"])
                ratings[i][1] = rating[0]["points"]
                i += 1

            # Simulates the Group
            winners = simulate_group(ratings)

            # Updates Group E with the teams points and new position
            for win in winners:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM groupE WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM groupE WHERE name = ?", win[1][0])
                    db.execute("UPDATE groupE SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE groupE SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM groupE WHERE name = ?", win[0])
                    db.execute("UPDATE groupE SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            teams = db.execute("SELECT * FROM groupE ORDER BY points DESC")
            position = 1
            for team in teams:
                db.execute("UPDATE groupE SET position = ? WHERE name = ?", position, team["name"])
                position += 1

            # Adds top two teams to groupWinners array
            for team in ratings:
                if team in groupWinners:
                    groupWinners.insert(groupWinners.index(team), "")
                    groupWinners.remove(team)
                if teams[0]["name"] == team[0]:
                    groupWinners.pop(4)
                    groupWinners.insert(4, team)
                if teams[1]["name"] == team[0]:
                    groupWinners.pop(9)
                    groupWinners.insert(9, team)

            return redirect("/finals")

        # Simulate Group F
        table = request.form.get("F")

        if table == "Simulate Group F":

            # resets group points to 0
            db.execute("UPDATE groupF SET points = 0")

            # Gathers groupF teams and their ratings
            groupF = db.execute("SELECT * FROM groupF ORDER BY position, points DESC")
            ratings = [[groupF[0]["name"], 0], [groupF[1]["name"], 0], [groupF[2]["name"], 0], [groupF[3]["name"], 0]]
            i = 0
            for team in groupF:
                rating = db.execute("SELECT name, points FROM teams WHERE id = ?", team["teams_id"])
                ratings[i][1] = rating[0]["points"]
                i += 1

            # Simulates the Group
            winners = simulate_group(ratings)

            # Updates Group F with the teams points and new position
            for win in winners:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM groupF WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM groupF WHERE name = ?", win[1][0])
                    db.execute("UPDATE groupF SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE groupF SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM groupF WHERE name = ?", win[0])
                    db.execute("UPDATE groupF SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            teams = db.execute("SELECT * FROM groupF ORDER BY points DESC")
            position = 1
            for team in teams:
                db.execute("UPDATE groupF SET position = ? WHERE name = ?", position, team["name"])
                position += 1

            # Adds top two teams to groupWinners array
            for team in ratings:
                if team in groupWinners:
                    groupWinners.insert(groupWinners.index(team), "")
                    groupWinners.remove(team)
                if teams[0]["name"] == team[0]:
                    groupWinners.pop(8)
                    groupWinners.insert(8, team)
                if teams[1]["name"] == team[0]:
                    groupWinners.pop(5)
                    groupWinners.insert(5, team)

            return redirect("/finals")

        # Simulate Group G
        table = request.form.get("G")

        if table == "Simulate Group G":

            # resets group points to 0
            db.execute("UPDATE groupG SET points = 0")

            # Gathers groupG teams and their ratings
            groupG = db.execute("SELECT * FROM groupG ORDER BY position, points DESC")
            ratings = [[groupG[0]["name"], 0], [groupG[1]["name"], 0], [groupG[2]["name"], 0], [groupG[3]["name"], 0]]
            i = 0
            for team in groupG:
                rating = db.execute("SELECT name, points FROM teams WHERE id = ?", team["teams_id"])
                ratings[i][1] = rating[0]["points"]
                i += 1

            # Simulates the Group
            winners = simulate_group(ratings)

            # Updates Group G with the teams points and new position
            for win in winners:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM groupG WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM groupG WHERE name = ?", win[1][0])
                    db.execute("UPDATE groupG SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE groupG SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM groupG WHERE name = ?", win[0])
                    db.execute("UPDATE groupG SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            teams = db.execute("SELECT * FROM groupG ORDER BY points DESC")
            position = 1
            for team in teams:
                db.execute("UPDATE groupG SET position = ? WHERE name = ?", position, team["name"])
                position += 1

            # Adds top two teams to groupWinners array
            for team in ratings:
                if team in groupWinners:
                    groupWinners.insert(groupWinners.index(team), "")
                    groupWinners.remove(team)
                if teams[0]["name"] == team[0]:
                    groupWinners.pop(6)
                    groupWinners.insert(6, team)
                if teams[1]["name"] == team[0]:
                    groupWinners.pop(11)
                    groupWinners.insert(11, team)

            return redirect("/finals")

        # Simulate Group H
        table = request.form.get("H")

        if table == "Simulate Group H":

            # resets group points to 0
            db.execute("UPDATE groupH SET points = 0")

            # Gathers groupH teams and their ratings
            groupH = db.execute("SELECT * FROM groupH ORDER BY position, points DESC")
            ratings = [[groupH[0]["name"], 0], [groupH[1]["name"], 0], [groupH[2]["name"], 0], [groupH[3]["name"], 0]]
            i = 0
            for team in groupH:
                rating = db.execute("SELECT name, points FROM teams WHERE id = ?", team["teams_id"])
                ratings[i][1] = rating[0]["points"]
                i += 1

            # Simulates the Group
            winners = simulate_group(ratings)

            # Updates Group H with the teams points and new position
            for win in winners:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM groupH WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM groupH WHERE name = ?", win[1][0])
                    db.execute("UPDATE groupH SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE groupH SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM groupH WHERE name = ?", win[0])
                    db.execute("UPDATE groupH SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            teams = db.execute("SELECT * FROM groupH ORDER BY points DESC")
            position = 1
            for team in teams:
                db.execute("UPDATE groupH SET position = ? WHERE name = ?", position, team["name"])
                position += 1

            # Adds top two teams to groupWinners array
            for team in ratings:
                if team in groupWinners:
                    groupWinners.insert(groupWinners.index(team), "")
                    groupWinners.remove(team)
                if teams[0]["name"] == team[0]:
                    groupWinners.pop(10)
                    groupWinners.insert(10, team)
                if teams[1]["name"] == team[0]:
                    groupWinners.pop(7)
                    groupWinners.insert(7, team)

            return redirect("/finals")



        return redirect("/finals")










@app.route("/conmebol", methods=["GET", "POST"])
def conmebol():
    """World Cup Qualifiers CONMEBOL"""

    if request.method == "GET":
        teams = db.execute("SELECT * FROM conmebol ORDER BY position, points DESC")
        return render_template("conmebol.html", teams=teams)

    if request.method == "POST":


        # resets group points to 0
        db.execute("UPDATE conmebol SET points = 0")

        # Gathers conmebol teams and their ratings
        conmebol = db.execute("SELECT name, rank FROM conmebol ORDER BY position, rank DESC")
        ratings = [[conmebol[0]["name"], conmebol[0]["rank"]], [conmebol[1]["name"], conmebol[1]["rank"]], [conmebol[2]["name"], conmebol[2]["rank"]], [conmebol[3]["name"], conmebol[3]["rank"]], [conmebol[4]["name"], conmebol[4]["rank"]], [conmebol[5]["name"], conmebol[5]["rank"]], [conmebol[6]["name"], conmebol[6]["rank"]], [conmebol[7]["name"], conmebol[7]["rank"]], [conmebol[8]["name"], conmebol[8]["rank"]], [conmebol[9]["name"], conmebol[9]["rank"]]]
        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates CONMEBOL with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM conmebol WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM conmebol WHERE name = ?", win[1][0])
                db.execute("UPDATE conmebol SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE conmebol SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM conmebol WHERE name = ?", win[0])
                db.execute("UPDATE conmebol SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM conmebol WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM conmebol WHERE name = ?", win[1][0])
                db.execute("UPDATE conmebol SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE conmebol SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM conmebol WHERE name = ?", win[0])
                db.execute("UPDATE conmebol SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute("SELECT * FROM conmebol ORDER BY points DESC")
        position = 1
        for team in teams:
            db.execute("UPDATE conmebol SET position = ? WHERE name = ?", position, team["name"])
            position += 1

        # Remove all CONMEBOL teams from the teams and playoff table
        db.execute("DELETE FROM teams WHERE conference = ?", "CONMEBOL")
        db.execute("DELETE FROM playoff WHERE conference = ?", "CONMEBOL")

        # Adds top 4 to finals
        qualified = db.execute("SELECT * FROM conmebol WHERE position < 5")
        for team in qualified:
                db.execute("INSERT INTO teams (id, name, points, conference) VALUES(?, ?, ?, ?)", team["id"], team["name"], team["rank"], "CONMEBOL")



        # Adds 5th place team to Intercontinental playoff
        db.execute("INSERT INTO playoff (id, name, rank, conference) VALUES(?, ?, ?, ?)", teams[4]["id"], teams[4]["name"], teams[4]["rank"], "CONMEBOL")

        # sets points to 0 for next group
        db.execute("UPDATE uefa SET points = 0")

        return redirect("/conmebol")

















@app.route("/uefa", methods=["GET", "POST"])
def uefa():
    """World Cup Qualifiers UEFA"""
    if request.method == "GET":

        # Gathers groups
        groupA = db.execute('SELECT * FROM uefa WHERE "group" = "A" ORDER BY "position", "points" DESC')
        groupB = db.execute('SELECT * FROM uefa WHERE "group" = "B" ORDER BY "position", "points" DESC')
        groupC = db.execute('SELECT * FROM uefa WHERE "group" = "C" ORDER BY "position", "points" DESC')
        groupD = db.execute('SELECT * FROM uefa WHERE "group" = "D" ORDER BY "position", "points" DESC')
        groupE = db.execute('SELECT * FROM uefa WHERE "group" = "E" ORDER BY "position", "points" DESC')
        groupF = db.execute('SELECT * FROM uefa WHERE "group" = "F" ORDER BY "position", "points" DESC')
        groupG = db.execute('SELECT * FROM uefa WHERE "group" = "G" ORDER BY "position", "points" DESC')
        groupH = db.execute('SELECT * FROM uefa WHERE "group" = "H" ORDER BY "position", "points" DESC')
        groupI = db.execute('SELECT * FROM uefa WHERE "group" = "I" ORDER BY "position", "points" DESC')
        groupJ = db.execute('SELECT * FROM uefa WHERE "group" = "J" ORDER BY "position", "points" DESC')

        # Adds second places teams and top ranked non-qualified teams to a group
        qualified = db.execute("SELECT * FROM uefa WHERE position = 1")

        second = db.execute("SELECT * FROM uefa WHERE position = 2 ORDER BY points DESC LIMIT 3")



        secondPlace = json.dumps(second)
        return render_template("uefa.html", a=groupA, b=groupB, c=groupC, d=groupD, e=groupE, f=groupF, g=groupG, h=groupH, i=groupI, j=groupJ, secondPlace=secondPlace)

    if request.method == "POST":

        # gathers all UEFA groups
        groupA = db.execute('SELECT * FROM uefa WHERE "group" = "A" ORDER BY "position", "points" DESC')
        groupB = db.execute('SELECT * FROM uefa WHERE "group" = "B" ORDER BY "position", "points" DESC')
        groupC = db.execute('SELECT * FROM uefa WHERE "group" = "C" ORDER BY "position", "points" DESC')
        groupD = db.execute('SELECT * FROM uefa WHERE "group" = "D" ORDER BY "position", "points" DESC')
        groupE = db.execute('SELECT * FROM uefa WHERE "group" = "E" ORDER BY "position", "points" DESC')
        groupF = db.execute('SELECT * FROM uefa WHERE "group" = "F" ORDER BY "position", "points" DESC')
        groupG = db.execute('SELECT * FROM uefa WHERE "group" = "G" ORDER BY "position", "points" DESC')
        groupH = db.execute('SELECT * FROM uefa WHERE "group" = "H" ORDER BY "position", "points" DESC')
        groupI = db.execute('SELECT * FROM uefa WHERE "group" = "I" ORDER BY "position", "points" DESC')
        groupJ = db.execute('SELECT * FROM uefa WHERE "group" = "J" ORDER BY "position", "points" DESC')






        # resets group points to 0
        db.execute('UPDATE uefa SET points = 0 WHERE "group" = "A"')

        # Gathers groupA teams and their ratings

        ratings = [[groupA[0]["name"], 0], [groupA[1]["name"], 0], [groupA[2]["name"], 0], [groupA[3]["name"], 0], [groupA[4]["name"], 0]]
        i = 0
        print(ratings)
        for team in groupA:
            rating = db.execute('SELECT name, points FROM uefa WHERE id = ? AND "group" = "A"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group A with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM uefa WHERE "group" = "A" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE uefa SET position = ? WHERE name = ?", position, team["name"])
            position += 1



        # resets group points to 0
        db.execute('UPDATE uefa SET points = 0 WHERE "group" = "B"')

        # Gathers groupA teams and their ratings

        ratings = [[groupB[0]["name"], 0], [groupB[1]["name"], 0], [groupB[2]["name"], 0], [groupB[3]["name"], 0], [groupB[4]["name"], 0]]
        i = 0

        for team in groupB:
            rating = db.execute('SELECT name, points FROM uefa WHERE id = ? AND "group" = "B"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group B with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM uefa WHERE "group" = "B" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE uefa SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE uefa SET points = 0 WHERE "group" = "C"')

        # Gathers groupC teams and their ratings

        ratings = [[groupC[0]["name"], 0], [groupC[1]["name"], 0], [groupC[2]["name"], 0], [groupC[3]["name"], 0], [groupC[4]["name"], 0]]
        i = 0

        for team in groupC:
            rating = db.execute('SELECT name, points FROM uefa WHERE id = ? AND "group" = "C"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group C with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM uefa WHERE "group" = "C" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE uefa SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE uefa SET points = 0 WHERE "group" = "D"')

        # Gathers groupD teams and their ratings

        ratings = [[groupD[0]["name"], 0], [groupD[1]["name"], 0], [groupD[2]["name"], 0], [groupD[3]["name"], 0], [groupD[4]["name"], 0]]
        i = 0
        for team in groupD:
            rating = db.execute('SELECT name, points FROM uefa WHERE id = ? AND "group" = "D"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group D with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM uefa WHERE "group" = "D" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE uefa SET position = ? WHERE name = ?", position, team["name"])
            position += 1



        # resets group points to 0
        db.execute('UPDATE uefa SET points = 0 WHERE "group" = "E"')

        # Gathers groupE teams and their ratings

        ratings = [[groupE[0]["name"], 0], [groupE[1]["name"], 0], [groupE[2]["name"], 0], [groupE[3]["name"], 0], [groupE[4]["name"], 0]]
        i = 0

        for team in groupE:
            rating = db.execute('SELECT name, points FROM uefa WHERE id = ? AND "group" = "E"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group E with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM uefa WHERE "group" = "E" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE uefa SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE uefa SET points = 0 WHERE "group" = "F"')

        # Gathers groupF teams and their ratings

        ratings = [[groupF[0]["name"], 0], [groupF[1]["name"], 0], [groupF[2]["name"], 0], [groupF[3]["name"], 0], [groupF[4]["name"], 0], [groupF[5]["name"], 0]]
        i = 0
        for team in groupF:
            rating = db.execute('SELECT name, points FROM uefa WHERE id = ? AND "group" = "F"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group F with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM uefa WHERE "group" = "F" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE uefa SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE uefa SET points = 0 WHERE "group" = "G"')

        # Gathers groupG teams and their ratings

        ratings = [[groupG[0]["name"], 0], [groupG[1]["name"], 0], [groupG[2]["name"], 0], [groupG[3]["name"], 0], [groupG[4]["name"], 0], [groupG[5]["name"], 0]]
        i = 0
        for team in groupG:
            rating = db.execute('SELECT name, points FROM uefa WHERE id = ? AND "group" = "G"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group G with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM uefa WHERE "group" = "G" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE uefa SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE uefa SET points = 0 WHERE "group" = "H"')

        # Gathers groupH teams and their ratings

        ratings = [[groupH[0]["name"], 0], [groupH[1]["name"], 0], [groupH[2]["name"], 0], [groupH[3]["name"], 0], [groupH[4]["name"], 0], [groupH[5]["name"], 0]]
        i = 0
        for team in groupH:
            rating = db.execute('SELECT name, points FROM uefa WHERE id = ? AND "group" = "H"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group H with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM uefa WHERE "group" = "H" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE uefa SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE uefa SET points = 0 WHERE "group" = "I"')

        # Gathers groupI teams and their ratings

        ratings = [[groupI[0]["name"], 0], [groupI[1]["name"], 0], [groupI[2]["name"], 0], [groupI[3]["name"], 0], [groupI[4]["name"], 0], [groupI[5]["name"], 0]]
        i = 0
        for team in groupI:
            rating = db.execute('SELECT name, points FROM uefa WHERE id = ? AND "group" = "I"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group I with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM uefa WHERE "group" = "I" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE uefa SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE uefa SET points = 0 WHERE "group" = "J"')

        # Gathers groupJ teams and their ratings

        ratings = [[groupJ[0]["name"], 0], [groupJ[1]["name"], 0], [groupJ[2]["name"], 0], [groupJ[3]["name"], 0], [groupJ[4]["name"], 0], [groupJ[5]["name"], 0]]
        i = 0
        for team in groupJ:
            rating = db.execute('SELECT name, points FROM uefa WHERE id = ? AND "group" = "J"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group J with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM uefa WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM uefa WHERE name = ?", win[1][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM uefa WHERE name = ?", win[0])
                db.execute("UPDATE uefa SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM uefa WHERE "group" = "J" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE uefa SET position = ? WHERE name = ?", position, team["name"])
            position += 1

        # Remove all UEFA teams from the teams table
        db.execute("DELETE FROM teams WHERE conference = ?", "UEFA")


        # Adds top team to finals
        qualified = db.execute("SELECT * FROM uefa WHERE position = 1")
        for team in qualified:
            db.execute("INSERT INTO teams (id, name, points, conference) VALUES(?, ?, ?, ?)", team["id"], team["name"], team["rank"], "UEFA")

        # Adds top 3 second place team to finals
        second = db.execute("SELECT * from uefa WHERE position = 2 ORDER BY points DESC LIMIT 3")
        for team in second:
            db.execute("INSERT INTO teams (id, name, points, conference) VALUES(?, ?, ?, ?)", team["id"], team["name"], team["rank"], "UEFA")



        return redirect("/uefa")


























@app.route("/concacaf", methods=["GET", "POST"])
def concacaf():
    """World Cup Qualifiers CONCACAF"""
    if request.method == "GET":

        # Gathers groups
        groupA = db.execute('SELECT * FROM concacaf WHERE "group" = "A" ORDER BY "position", "points" DESC')
        groupB = db.execute('SELECT * FROM concacaf WHERE "group" = "B" ORDER BY "position", "points" DESC')
        groupC = db.execute('SELECT * FROM concacaf WHERE "group" = "C" ORDER BY "position", "points" DESC')
        groupD = db.execute('SELECT * FROM concacaf WHERE "group" = "D" ORDER BY "position", "points" DESC')
        groupE = db.execute('SELECT * FROM concacaf WHERE "group" = "E" ORDER BY "position", "points" DESC')
        groupF = db.execute('SELECT * FROM concacaf WHERE "group" = "F" ORDER BY "position", "points" DESC')



        round3 = db.execute('SELECT * FROM concacaf WHERE position = 1 and "group" != " " ORDER BY "group"')
        seeded = db.execute('SELECT * FROM concacaf WHERE "group" == " "')


        round3 = json.dumps(round3)
        seeded = json.dumps(seeded)


        return render_template("concacaf.html", a=groupA, b=groupB, c=groupC, d=groupD, e=groupE, f=groupF, round3=round3, seeded=seeded)

    if request.method == "POST":

        # gathers all concacaf groups
        groupA = db.execute('SELECT * FROM concacaf WHERE "group" = "A" ORDER BY "position", "points" DESC')
        groupB = db.execute('SELECT * FROM concacaf WHERE "group" = "B" ORDER BY "position", "points" DESC')
        groupC = db.execute('SELECT * FROM concacaf WHERE "group" = "C" ORDER BY "position", "points" DESC')
        groupD = db.execute('SELECT * FROM concacaf WHERE "group" = "D" ORDER BY "position", "points" DESC')
        groupE = db.execute('SELECT * FROM concacaf WHERE "group" = "E" ORDER BY "position", "points" DESC')
        groupF = db.execute('SELECT * FROM concacaf WHERE "group" = "F" ORDER BY "position", "points" DESC')


        # adds winners to the finals database
        winners = request.get_json()
        if winners != None:
            for winner in winners:
                if winner["position"] != 4:
                    db.execute("INSERT INTO teams (id, name, points, conference) VALUES(?, ?, ?, ?)", winner["id"], winner["name"], winner["rank"], "CONCACAF")
                else:
                    db.execute("INSERT INTO playoff (id, name, rank, conference) VALUES(?, ?, ?, ?)", winner["id"], winner["name"], winner["rank"], "CONCACAF")



        # Simulate Round 1
        table = request.form.get("All")

        if table == "Simulate Round 1":

            # resets group points to 0
            db.execute('UPDATE concacaf SET points = 0 WHERE "group" = "A"')

            # Gathers groupA teams and their ratings

            ratings = [[groupA[0]["name"], 0], [groupA[1]["name"], 0], [groupA[2]["name"], 0], [groupA[3]["name"], 0], [groupA[4]["name"], 0]]
            i = 0

            for team in groupA:
                rating = db.execute('SELECT name, points FROM concacaf WHERE id = ? AND "group" = "A"', team["id"])
                ratings[i][1] = rating[0]["points"]
                i += 1

            # Simulates the Group
            homeGames = simulate_group(ratings)
            awayGames = simulate_group(ratings)

            # Updates Group A with the teams points and new position
            for win in homeGames:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[1][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            for win in awayGames:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[1][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            teams = db.execute('SELECT * FROM concacaf WHERE "group" = "A" ORDER BY points DESC')
            position = 1
            for team in teams:
                db.execute("UPDATE concacaf SET position = ? WHERE name = ?", position, team["name"])
                position += 1



            # resets group points to 0
            db.execute('UPDATE concacaf SET points = 0 WHERE "group" = "B"')

            # Gathers groupA teams and their ratings

            ratings = [[groupB[0]["name"], 0], [groupB[1]["name"], 0], [groupB[2]["name"], 0], [groupB[3]["name"], 0], [groupB[4]["name"], 0]]
            i = 0

            for team in groupB:
                rating = db.execute('SELECT name, points FROM concacaf WHERE id = ? AND "group" = "B"', team["id"])
                ratings[i][1] = rating[0]["points"]
                i += 1

            # Simulates the Group
            homeGames = simulate_group(ratings)
            awayGames = simulate_group(ratings)

            # Updates Group B with the teams points and new position
            for win in homeGames:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[1][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            for win in awayGames:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[1][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            teams = db.execute('SELECT * FROM concacaf WHERE "group" = "B" ORDER BY points DESC')
            position = 1
            for team in teams:
                db.execute("UPDATE concacaf SET position = ? WHERE name = ?", position, team["name"])
                position += 1


            # resets group points to 0
            db.execute('UPDATE concacaf SET points = 0 WHERE "group" = "C"')

            # Gathers groupC teams and their ratings

            ratings = [[groupC[0]["name"], 0], [groupC[1]["name"], 0], [groupC[2]["name"], 0], [groupC[3]["name"], 0], [groupC[4]["name"], 0]]
            i = 0

            for team in groupC:
                rating = db.execute('SELECT name, points FROM concacaf WHERE id = ? AND "group" = "C"', team["id"])
                ratings[i][1] = rating[0]["points"]
                i += 1

            # Simulates the Group
            homeGames = simulate_group(ratings)
            awayGames = simulate_group(ratings)

            # Updates Group C with the teams points and new position
            for win in homeGames:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[1][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            for win in awayGames:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[1][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            teams = db.execute('SELECT * FROM concacaf WHERE "group" = "C" ORDER BY points DESC')
            position = 1
            for team in teams:
                db.execute("UPDATE concacaf SET position = ? WHERE name = ?", position, team["name"])
                position += 1


            # resets group points to 0
            db.execute('UPDATE concacaf SET points = 0 WHERE "group" = "D"')

            # Gathers groupD teams and their ratings

            ratings = [[groupD[0]["name"], 0], [groupD[1]["name"], 0], [groupD[2]["name"], 0], [groupD[3]["name"], 0], [groupD[4]["name"], 0]]
            i = 0
            for team in groupD:
                rating = db.execute('SELECT name, points FROM concacaf WHERE id = ? AND "group" = "D"', team["id"])
                ratings[i][1] = rating[0]["points"]
                i += 1

            # Simulates the Group
            homeGames = simulate_group(ratings)
            awayGames = simulate_group(ratings)

            # Updates Group D with the teams points and new position
            for win in homeGames:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[1][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            for win in awayGames:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[1][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            teams = db.execute('SELECT * FROM concacaf WHERE "group" = "D" ORDER BY points DESC')
            position = 1
            for team in teams:
                db.execute("UPDATE concacaf SET position = ? WHERE name = ?", position, team["name"])
                position += 1



            # resets group points to 0
            db.execute('UPDATE concacaf SET points = 0 WHERE "group" = "E"')

            # Gathers groupE teams and their ratings

            ratings = [[groupE[0]["name"], 0], [groupE[1]["name"], 0], [groupE[2]["name"], 0], [groupE[3]["name"], 0], [groupE[4]["name"], 0]]
            i = 0

            for team in groupE:
                rating = db.execute('SELECT name, points FROM concacaf WHERE id = ? AND "group" = "E"', team["id"])
                ratings[i][1] = rating[0]["points"]
                i += 1

            # Simulates the Group
            homeGames = simulate_group(ratings)
            awayGames = simulate_group(ratings)

            # Updates Group E with the teams points and new position
            for win in homeGames:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[1][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            for win in awayGames:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[1][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            teams = db.execute('SELECT * FROM concacaf WHERE "group" = "E" ORDER BY points DESC')
            position = 1
            for team in teams:
                db.execute("UPDATE concacaf SET position = ? WHERE name = ?", position, team["name"])
                position += 1


            # resets group points to 0
            db.execute('UPDATE concacaf SET points = 0 WHERE "group" = "F"')

            # Gathers groupF teams and their ratings

            ratings = [[groupF[0]["name"], 0], [groupF[1]["name"], 0], [groupF[2]["name"], 0], [groupF[3]["name"], 0], [groupF[4]["name"], 0]]
            i = 0
            for team in groupF:
                rating = db.execute('SELECT name, points FROM concacaf WHERE id = ? AND "group" = "F"', team["id"])
                ratings[i][1] = rating[0]["points"]
                i += 1

            # Simulates the Group
            homeGames = simulate_group(ratings)
            awayGames = simulate_group(ratings)

            # Updates Group F with the teams points and new position
            for win in homeGames:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[1][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            for win in awayGames:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[1][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            teams = db.execute('SELECT * FROM concacaf WHERE "group" = "F" ORDER BY points DESC')
            position = 1
            for team in teams:
                db.execute("UPDATE concacaf SET position = ? WHERE name = ?", position, team["name"])
                position += 1



        table = request.form.get("round3")

        if table == "Simulate Round 3":
            #clears points
            db.execute("UPDATE concacaf SET points = 0")

            # Gathers winners from Round 1
            winners = db.execute('SELECT * FROM concacaf WHERE position = 1 ORDER BY "group"')
            # Gathers seeded teams to round 3
            round3 = db.execute('SELECT * FROM concacaf ORDER BY "group" LIMIT 5')

            # Gathers winner teams and their ratings

            ratings = [[winners[0]["name"], 0], [winners[1]["name"], 0], [winners[2]["name"], 0], [winners[3]["name"], 0], [winners[4]["name"], 0], [winners[5]["name"], 0]]
            i = 0
            for team in winners:
                rating = db.execute('SELECT name, points FROM concacaf WHERE id = ?', team["id"])
                ratings[i][1] = rating[0]["points"]
                i += 1
            if simulate_game(ratings[0], ratings[5]):
                round3.append(winners[0])
            else: round3.append(winners[5])
            if simulate_game(ratings[1], ratings[4]):
                round3.append(winners[1])
            else: round3.append(winners[4])
            if simulate_game(ratings[2], ratings[3]):
                round3.append(winners[2])
            else: round3.append(winners[3])

            print(round3)


            # Gathers round 3 teams and their ratings

            ratings = [[round3[0]["name"], 0], [round3[1]["name"], 0], [round3[2]["name"], 0], [round3[3]["name"], 0], [round3[4]["name"], 0], [round3[5]["name"], 0], [round3[6]["name"], 0], [round3[7]["name"], 0]]
            i = 0

            for team in round3:
                rating = db.execute('SELECT name, points FROM concacaf WHERE id = ?', team["id"])
                ratings[i][1] = rating[0]["points"]
                i += 1

            # Simulates the Group
            homeGames = simulate_group(ratings)
            awayGames = simulate_group(ratings)

            # Updates Round 3 with the teams points and new position
            for win in homeGames:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[1][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            for win in awayGames:
                if len(win[0]) == 2:
                    points1 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0][0])
                    points2 = db.execute("SELECT points FROM concacaf WHERE name = ?", win[1][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
                else:
                    points = db.execute("SELECT points FROM concacaf WHERE name = ?", win[0])
                    db.execute("UPDATE concacaf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
            for team in round3:
                db.execute("UPDATE concacaf SET position = 1 WHERE id = ?", team["id"])





        return redirect("/concacaf")



























@app.route("/caf", methods=["GET", "POST"])
def caf():
    """World Cup Qualifiers CAF"""

    if request.method == "GET":

        # Gathers groups
        groupA = db.execute('SELECT * FROM caf WHERE "group" = "A" ORDER BY "position", "points" DESC')
        groupB = db.execute('SELECT * FROM caf WHERE "group" = "B" ORDER BY "position", "points" DESC')
        groupC = db.execute('SELECT * FROM caf WHERE "group" = "C" ORDER BY "position", "points" DESC')
        groupD = db.execute('SELECT * FROM caf WHERE "group" = "D" ORDER BY "position", "points" DESC')
        groupE = db.execute('SELECT * FROM caf WHERE "group" = "E" ORDER BY "position", "points" DESC')
        groupF = db.execute('SELECT * FROM caf WHERE "group" = "F" ORDER BY "position", "points" DESC')
        groupG = db.execute('SELECT * FROM caf WHERE "group" = "G" ORDER BY "position", "points" DESC')
        groupH = db.execute('SELECT * FROM caf WHERE "group" = "H" ORDER BY "position", "points" DESC')
        groupI = db.execute('SELECT * FROM caf WHERE "group" = "I" ORDER BY "position", "points" DESC')
        groupJ = db.execute('SELECT * FROM caf WHERE "group" = "J" ORDER BY "position", "points" DESC')

        # Adds second places teams and top ranked non-qualified teams to a group
        qualified = db.execute("SELECT * FROM caf WHERE position = 1 ORDER BY rank DESC")

        # removes qualified teams if groups haven't been simulated.
        points = 0
        for team in groupA:
            points += team["points"]
        if points == 0:
            qualified = []


        winners = json.dumps(qualified)


        return render_template("caf.html", a=groupA, b=groupB, c=groupC, d=groupD, e=groupE, f=groupF, g=groupG, h=groupH, i=groupI, j=groupJ, qualified=qualified, winners=winners)

    if request.method == "POST":

        # gathers all CAF groups
        groupA = db.execute('SELECT * FROM caf WHERE "group" = "A" ORDER BY "position", "points" DESC')
        groupB = db.execute('SELECT * FROM caf WHERE "group" = "B" ORDER BY "position", "points" DESC')
        groupC = db.execute('SELECT * FROM caf WHERE "group" = "C" ORDER BY "position", "points" DESC')
        groupD = db.execute('SELECT * FROM caf WHERE "group" = "D" ORDER BY "position", "points" DESC')
        groupE = db.execute('SELECT * FROM caf WHERE "group" = "E" ORDER BY "position", "points" DESC')
        groupF = db.execute('SELECT * FROM caf WHERE "group" = "F" ORDER BY "position", "points" DESC')
        groupG = db.execute('SELECT * FROM caf WHERE "group" = "G" ORDER BY "position", "points" DESC')
        groupH = db.execute('SELECT * FROM caf WHERE "group" = "H" ORDER BY "position", "points" DESC')
        groupI = db.execute('SELECT * FROM caf WHERE "group" = "I" ORDER BY "position", "points" DESC')
        groupJ = db.execute('SELECT * FROM caf WHERE "group" = "J" ORDER BY "position", "points" DESC')



        winners = request.get_json()
        if winners != None:
            for winner in winners:
                db.execute("INSERT INTO teams (id, name, points, conference) VALUES(?, ?, ?, ?)", winner["id"], winner["name"], winner["rank"], "CAF")



        # resets group points to 0
        db.execute('UPDATE caf SET points = 0 WHERE "group" = "A"')

        # Gathers groupA teams and their ratings

        ratings = [[groupA[0]["name"], 0], [groupA[1]["name"], 0], [groupA[2]["name"], 0], [groupA[3]["name"], 0]]
        i = 0

        for team in groupA:
            rating = db.execute('SELECT name, points FROM caf WHERE id = ? AND "group" = "A"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group A with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM caf WHERE "group" = "A" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE caf SET position = ? WHERE name = ?", position, team["name"])
            position += 1



        # resets group points to 0
        db.execute('UPDATE caf SET points = 0 WHERE "group" = "B"')

        # Gathers groupB teams and their ratings

        ratings = [[groupB[0]["name"], 0], [groupB[1]["name"], 0], [groupB[2]["name"], 0], [groupB[3]["name"], 0]]
        i = 0

        for team in groupB:
            rating = db.execute('SELECT name, points FROM caf WHERE id = ? AND "group" = "B"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group B with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM caf WHERE "group" = "B" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE caf SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE caf SET points = 0 WHERE "group" = "C"')

        # Gathers groupC teams and their ratings

        ratings = [[groupC[0]["name"], 0], [groupC[1]["name"], 0], [groupC[2]["name"], 0], [groupC[3]["name"], 0]]
        i = 0

        for team in groupC:
            rating = db.execute('SELECT name, points FROM caf WHERE id = ? AND "group" = "C"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group C with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM caf WHERE "group" = "C" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE caf SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE caf SET points = 0 WHERE "group" = "D"')

        # Gathers groupD teams and their ratings

        ratings = [[groupD[0]["name"], 0], [groupD[1]["name"], 0], [groupD[2]["name"], 0], [groupD[3]["name"], 0]]
        i = 0
        for team in groupD:
            rating = db.execute('SELECT name, points FROM caf WHERE id = ? AND "group" = "D"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group D with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM caf WHERE "group" = "D" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE caf SET position = ? WHERE name = ?", position, team["name"])
            position += 1



        # resets group points to 0
        db.execute('UPDATE caf SET points = 0 WHERE "group" = "E"')

        # Gathers groupE teams and their ratings

        ratings = [[groupE[0]["name"], 0], [groupE[1]["name"], 0], [groupE[2]["name"], 0], [groupE[3]["name"], 0]]
        i = 0

        for team in groupE:
            rating = db.execute('SELECT name, points FROM caf WHERE id = ? AND "group" = "E"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group E with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM caf WHERE "group" = "E" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE caf SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE caf SET points = 0 WHERE "group" = "F"')

        # Gathers groupF teams and their ratings

        ratings = [[groupF[0]["name"], 0], [groupF[1]["name"], 0], [groupF[2]["name"], 0], [groupF[3]["name"], 0]]
        i = 0
        for team in groupF:
            rating = db.execute('SELECT name, points FROM caf WHERE id = ? AND "group" = "F"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group F with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM caf WHERE "group" = "F" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE caf SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE caf SET points = 0 WHERE "group" = "G"')

        # Gathers groupG teams and their ratings

        ratings = [[groupG[0]["name"], 0], [groupG[1]["name"], 0], [groupG[2]["name"], 0], [groupG[3]["name"], 0]]
        i = 0
        for team in groupG:
            rating = db.execute('SELECT name, points FROM caf WHERE id = ? AND "group" = "G"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group G with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM caf WHERE "group" = "G" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE caf SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE caf SET points = 0 WHERE "group" = "H"')

        # Gathers groupH teams and their ratings

        ratings = [[groupH[0]["name"], 0], [groupH[1]["name"], 0], [groupH[2]["name"], 0], [groupH[3]["name"], 0]]
        i = 0
        for team in groupH:
            rating = db.execute('SELECT name, points FROM caf WHERE id = ? AND "group" = "H"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group H with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM caf WHERE "group" = "H" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE caf SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE caf SET points = 0 WHERE "group" = "I"')

        # Gathers groupI teams and their ratings

        ratings = [[groupI[0]["name"], 0], [groupI[1]["name"], 0], [groupI[2]["name"], 0], [groupI[3]["name"], 0]]
        i = 0
        for team in groupI:
            rating = db.execute('SELECT name, points FROM caf WHERE id = ? AND "group" = "I"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group I with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM caf WHERE "group" = "I" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE caf SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE caf SET points = 0 WHERE "group" = "J"')

        # Gathers groupJ teams and their ratings

        ratings = [[groupJ[0]["name"], 0], [groupJ[1]["name"], 0], [groupJ[2]["name"], 0], [groupJ[3]["name"], 0]]
        i = 0
        for team in groupJ:
            rating = db.execute('SELECT name, points FROM caf WHERE id = ? AND "group" = "J"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group J with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM caf WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM caf WHERE name = ?", win[1][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM caf WHERE name = ?", win[0])
                db.execute("UPDATE caf SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM caf WHERE "group" = "J" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE caf SET position = ? WHERE name = ?", position, team["name"])
            position += 1








        return redirect("/caf")


















@app.route("/afc", methods=["GET", "POST"])
def afc():
    """World Cup Qualifiers AFC"""
    if request.method == "GET":

        # Gathers groups
        groupA = db.execute('SELECT * FROM afc WHERE "group" = "A" ORDER BY "position", "points" DESC')
        groupB = db.execute('SELECT * FROM afc WHERE "group" = "B" ORDER BY "position", "points" DESC')
        groupC = db.execute('SELECT * FROM afc WHERE "group" = "C" ORDER BY "position", "points" DESC')
        groupD = db.execute('SELECT * FROM afc WHERE "group" = "D" ORDER BY "position", "points" DESC')
        groupE = db.execute('SELECT * FROM afc WHERE "group" = "E" ORDER BY "position", "points" DESC')
        groupF = db.execute('SELECT * FROM afc WHERE "group" = "F" ORDER BY "position", "points" DESC')
        groupG = db.execute('SELECT * FROM afc WHERE "group" = "G" ORDER BY "position", "points" DESC')
        groupH = db.execute('SELECT * FROM afc WHERE "group" = "H" ORDER BY "position", "points" DESC')


        # Adds second places teams and top ranked non-qualified teams to a group
        qualified = db.execute("SELECT * FROM afc WHERE position = 1 ORDER BY rank DESC")
        i = 0
        qatar = False
        second = db.execute("SELECT * FROM afc WHERE position = 2 ORDER BY points DESC LIMIT 5")
        for team in qualified:
            print(team["id"])
            if team["id"] == 178:
                print("found")
                qualified.pop(i)

                qatar = True
                break
            i += 1
        j = 0
        for team in second:
            if qatar == True:
                break
            if team["id"] == 178:
                second.pop(j)
                qatar = True
                break
            j += 1
        if qatar == False:
            second.pop(4)


        finalGroups = qualified + second






        finalists = json.dumps(finalGroups)


        return render_template("afc.html", a=groupA, b=groupB, c=groupC, d=groupD, e=groupE, f=groupF, g=groupG, h=groupH, finalists=finalists)

    if request.method == "POST":

        # gathers all AFC groups
        groupA = db.execute('SELECT * FROM afc WHERE "group" = "A" ORDER BY "position", "points" DESC')
        groupB = db.execute('SELECT * FROM afc WHERE "group" = "B" ORDER BY "position", "points" DESC')
        groupC = db.execute('SELECT * FROM afc WHERE "group" = "C" ORDER BY "position", "points" DESC')
        groupD = db.execute('SELECT * FROM afc WHERE "group" = "D" ORDER BY "position", "points" DESC')
        groupE = db.execute('SELECT * FROM afc WHERE "group" = "E" ORDER BY "position", "points" DESC')
        groupF = db.execute('SELECT * FROM afc WHERE "group" = "F" ORDER BY "position", "points" DESC')
        groupG = db.execute('SELECT * FROM afc WHERE "group" = "G" ORDER BY "position", "points" DESC')
        groupH = db.execute('SELECT * FROM afc WHERE "group" = "H" ORDER BY "position", "points" DESC')

        qatar = db.execute("SELECT * FROM afc WHERE name = ?", "Qatar")

        i = 0
        winners = request.get_json()
        if winners != None:
            for winner in winners:
                i += 1
                if i == 5:
                    db.execute("INSERT INTO playoff (id, name, rank, conference) VALUES (?, ?, ?, ?)", winner["id"], winner["name"], winner["rank"], "AFC")
                db.execute("INSERT INTO teams (id, name, points, conference) VALUES(?, ?, ?, ?)", winner["id"], winner["name"], winner["rank"], "AFC")
            db.execute("INSERT INTO teams (id, name, points, conference) VALUES(?, ?, ?, ?)", qatar[0]["id"], qatar[0]["name"], qatar[0]["rank"], "AFC")



        # resets group points to 0
        db.execute('UPDATE afc SET points = 0 WHERE "group" = "A"')

        # Gathers groupA teams and their ratings

        ratings = [[groupA[0]["name"], 0], [groupA[1]["name"], 0], [groupA[2]["name"], 0], [groupA[3]["name"], 0], [groupA[4]["name"], 0]]
        i = 0

        for team in groupA:
            rating = db.execute('SELECT name, points FROM afc WHERE id = ? AND "group" = "A"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group A with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM afc WHERE "group" = "A" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE afc SET position = ? WHERE name = ?", position, team["name"])
            position += 1



        # resets group points to 0
        db.execute('UPDATE afc SET points = 0 WHERE "group" = "B"')

        # Gathers groupB teams and their ratings

        ratings = [[groupB[0]["name"], 0], [groupB[1]["name"], 0], [groupB[2]["name"], 0], [groupB[3]["name"], 0], [groupB[4]["name"], 0]]
        i = 0

        for team in groupB:
            rating = db.execute('SELECT name, points FROM afc WHERE id = ? AND "group" = "B"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group B with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM afc WHERE "group" = "B" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE afc SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE afc SET points = 0 WHERE "group" = "C"')

        # Gathers groupC teams and their ratings

        ratings = [[groupC[0]["name"], 0], [groupC[1]["name"], 0], [groupC[2]["name"], 0], [groupC[3]["name"], 0], [groupC[4]["name"], 0]]
        i = 0

        for team in groupC:
            rating = db.execute('SELECT name, points FROM afc WHERE id = ? AND "group" = "C"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group C with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM afc WHERE "group" = "C" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE afc SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE afc SET points = 0 WHERE "group" = "D"')

        # Gathers groupD teams and their ratings

        ratings = [[groupD[0]["name"], 0], [groupD[1]["name"], 0], [groupD[2]["name"], 0], [groupD[3]["name"], 0], [groupD[3]["name"], 0]]
        i = 0
        for team in groupD:
            rating = db.execute('SELECT name, points FROM afc WHERE id = ? AND "group" = "D"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group D with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM afc WHERE "group" = "D" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE afc SET position = ? WHERE name = ?", position, team["name"])
            position += 1



        # resets group points to 0
        db.execute('UPDATE afc SET points = 0 WHERE "group" = "E"')

        # Gathers groupE teams and their ratings

        ratings = [[groupE[0]["name"], 0], [groupE[1]["name"], 0], [groupE[2]["name"], 0], [groupE[3]["name"], 0], [groupE[4]["name"], 0]]
        i = 0

        for team in groupE:
            rating = db.execute('SELECT name, points FROM afc WHERE id = ? AND "group" = "E"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group E with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM afc WHERE "group" = "E" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE afc SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE afc SET points = 0 WHERE "group" = "F"')

        # Gathers groupF teams and their ratings

        ratings = [[groupF[0]["name"], 0], [groupF[1]["name"], 0], [groupF[2]["name"], 0], [groupF[3]["name"], 0], [groupF[4]["name"], 0]]
        i = 0
        for team in groupF:
            rating = db.execute('SELECT name, points FROM afc WHERE id = ? AND "group" = "F"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group F with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM afc WHERE "group" = "F" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE afc SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE afc SET points = 0 WHERE "group" = "G"')

        # Gathers groupG teams and their ratings

        ratings = [[groupG[0]["name"], 0], [groupG[1]["name"], 0], [groupG[2]["name"], 0], [groupG[3]["name"], 0], [groupG[4]["name"], 0]]
        i = 0
        for team in groupG:
            rating = db.execute('SELECT name, points FROM afc WHERE id = ? AND "group" = "G"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group G with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM afc WHERE "group" = "G" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE afc SET position = ? WHERE name = ?", position, team["name"])
            position += 1


        # resets group points to 0
        db.execute('UPDATE afc SET points = 0 WHERE "group" = "H"')

        # Gathers groupH teams and their ratings

        ratings = [[groupH[0]["name"], 0], [groupH[1]["name"], 0], [groupH[2]["name"], 0], [groupH[3]["name"], 0]]
        i = 0
        for team in groupH:
            rating = db.execute('SELECT name, points FROM afc WHERE id = ? AND "group" = "H"', team["id"])
            ratings[i][1] = rating[0]["points"]
            i += 1

        # Simulates the Group
        homeGames = simulate_group(ratings)
        awayGames = simulate_group(ratings)

        # Updates Group H with the teams points and new position
        for win in homeGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        for win in awayGames:
            if len(win[0]) == 2:
                points1 = db.execute("SELECT points FROM afc WHERE name = ?", win[0][0])
                points2 = db.execute("SELECT points FROM afc WHERE name = ?", win[1][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points1[0]["points"], win[0][0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 1 + points2[0]["points"], win[1][0])
            else:
                points = db.execute("SELECT points FROM afc WHERE name = ?", win[0])
                db.execute("UPDATE afc SET points = ? WHERE name = ?", 3 + points[0]["points"], win[0])
        teams = db.execute('SELECT * FROM afc WHERE "group" = "H" ORDER BY points DESC')
        position = 1
        for team in teams:
            db.execute("UPDATE afc SET position = ? WHERE name = ?", position, team["name"])
            position += 1









        return redirect("/afc")























@app.route("/playoff", methods=["GET", "POST"])
def playoff():
    """World Cup Qualifiers Playoff"""
    if request.method == "GET":

        # Gathers groups
        playoffPython = db.execute('SELECT * FROM playoff')






        playoffJSON = json.dumps(playoffPython)


        return render_template("playoff.html", playoffPython=playoffPython, playoffJSON=playoffJSON)

    if request.method == "POST":

        i = 0
        winners = request.get_json()
        for team in winners:
            db.execute("INSERT INTO teams (id, name, points, conference) VALUES(?, ?, ?, ?)", team["id"], team["name"], team["rank"], team["conference"])

        return redirect("/playoff")

