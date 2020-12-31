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
print(correct_schedules["Hawaii-Pacific"])
print(correct_schedules["Hawaii"])
#print(correct_schedules["McNeese State"])

# who to root for
def root_for(fav_team, team1, team2, schedules):
    return root_for_help([fav_team], team1, team2, schedules, 1)

map1 = []
map2 = []
# what about infinite loops?????
def root_for_help(teams, team1, team2, schedules, order):
    print(order)
    newteams = []
    order1_count = 0
    order2_count = 0
    for team in teams:
        
        for nextteam in schedules[team]:
            
            if nextteam == team1:
                order1_count += 1
                map1.append((team, order))
            if nextteam == team2:
                order2_count += 1
                map2.append((team, order))
            newteams.append(nextteam)
        
    if order1_count > order2_count:
        print(map1)
        print(map2)
        print(order1_count)
        print(order2_count)
        return team1
    elif order2_count > order1_count:
        print(map1)
        print(map2)
        print(order1_count)
        print(order2_count)
        return team2
    else:
        return root_for_help(newteams, team1, team2, schedules, order + 1)



# what about infinite loops?????
def root_for_help_2(teams, team1, schedules, order):
    print(order)
    newteams = []
    order1_count = 0
    i = 0
    for team in teams:
        
        if i % 100000 == 0:
            print(str(i) + 'teams processed')
            
        i += 1
        for nextteam in schedules[team]:


            if nextteam == team1:
                order1_count += 1
                map1.append((team, order))
            newteams.append(nextteam)

    if order1_count > 0:
        return (order, order1_count, team1)
    else:
        return root_for_help_2(newteams, team1, schedules, order + 1)

min = [0,0]
least_favorite_team = 'string'
for team in correct_schedules:
    (order, count, team) = root_for_help_2(['Lamar'], team, correct_schedules, 1)
    if order > min[0]:
        min[0] = order
        min[1] = count
        least_favorite_team = str(team)
    elif order == min[0] and count < min[1]:
        min[1] = count
        least_favorite_team = str(team)

print(least_favorite_team)
print(min)


# print(root_for_help_2(["Northeastern"], team1, schedules, order))

print(root_for("Lamar", "Lehigh", "Hawaii-Pacific", correct_schedules))