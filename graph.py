# Goal: create graph from db

import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
conn = psycopg2.connect(
    host=os.getenv("HOST"),
    database=os.getenv("DATABASE"),
    user=os.getenv("DB_USER"),
    password=os.getenv("PASSWORD"),
    port=os.getenv("PORT"))

cur = conn.cursor()
cur.execute("SELECT * from games")
games = cur.fetchall()

def format_games(games):
    newgames = []
    for game in games:
        newgames.append((game[0][1:], game[1][1:]))
    return newgames

def schedules(games):
    schedules = {}
    for game in games:
        if game[0] not in schedules:
            schedules[game[0]] = []
        schedules[game[0]].append(game[1])
    
        if game[1] not in schedules:
            schedules[game[1]] = []
        schedules[game[1]].append(game[0])
    return schedules


correct_schedules = schedules(format_games(games))
print(correct_schedules["Northeastern"])

# who to root for
def root_for(fav_team, team1, team2, schedules):
    order1_count = 0
    order2_count = 0
    for team in schedules[fav_team]:
        if team == team1:
            order1_count += 1
        if team == team2:
            order2_count += 1
        
    if order1_count > order2_count:
        return team1
    elif order2_count > order1_count:
        return team2
    else:
        return "tie"

print(root_for("Northeastern", "Syracuse", "Georgia", correct_schedules))