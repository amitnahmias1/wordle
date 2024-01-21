
### leaderboard.py

from pymongo import MongoClient


green = [47,181,83]
def find_stats(user):
    db = client['wordle'] if langEN else client['hewordle']
    dates = []
    for item in db.list_collection_names():
        if len(item) == 10:
            dates.append(item)
    all_dates = sorted(dates)

    plays_count = 0
    avg = 0
    wins = 0
    sum = 0
    for date in all_dates:
        date_collection = db[date]
        cursor = date_collection.find({'user': user})
        for play in cursor:
            if len(play['colors']) == 1 and play['colors'][-1] == [green for _ in range(5)]:
                print(f'user {user} cheated!')
            else:
                if play['colors'][-1] == [green for _ in range(5)]:
                    wins += 1
                    sum += len(play['colors'])
                plays_count += 1
    if wins != 0:
        avg = round(sum / wins, 2)
    winners_collection = db["winners"]
    cursor = winners_collection.find({})
    winnings = 0
    for day in cursor:
        if user in day['users']:
            winnings += 1
    return [plays_count, wins, avg, winnings]

for a in [True, False]:
    langEN = a
    client = MongoClient('mongodb://root:wordle@mongodb:27017/')
    db = client['wordle'] if langEN else client['hewordle']
    leaderboard_collection = db["leaderboard"]
    dates = []
    for item in db.list_collection_names():
        if len(item) == 10:
            dates.append(item)
    all_dates = sorted(dates)

    all_users = []
    for date in all_dates:
        date_collection = db[date]
        cursor = date_collection.find({})
        for play in cursor:
            user = play['user']
            if user[0] != 'x' and user[0] != 'X' and user[0] != 'm' and user not in all_users:
                all_users.append(user)

    all_plays_count = {}
    all_wins = {}
    all_avg = {}
    all_winnings = {}
    all_overall = {}
    for user in all_users:
        stats = find_stats(user)
        # print(stats, type(stats[0]))
        all_plays_count[user] = stats[0]
        all_wins[user] = stats[1]
        if stats[0] >= 7:
            all_avg[user] = stats[2]
        all_winnings[user] = stats[3]
        if stats[0] >= 7:
            overall = (stats[1]/stats[0])*300 + stats[0]*1.2 + stats[3]*2 + (6-stats[2])*200
            all_overall[user] = overall

    all_plays_count = dict(sorted(all_plays_count.items(), key=lambda pair: pair[1], reverse=True))
    all_wins = dict(sorted(all_wins.items(), key=lambda pair: pair[1], reverse=True))
    all_avg = dict(sorted(all_avg.items(), key=lambda pair: pair[1]))
    all_winnings = dict(sorted(all_winnings.items(), key=lambda pair: pair[1], reverse=True))
    all_overall = dict(sorted(all_overall.items(), key=lambda pair: pair[1], reverse=True))

    all_plays_count['type'] = 'plays_count'
    all_wins['type'] = 'wins_count'
    all_avg['type'] = 'avg'
    all_winnings['type'] = 'winnings'
    all_overall['type'] = 'overall'

    try:
        db["leaderboard"].drop()
    except:
        pass

    _ = leaderboard_collection.insert_one(all_plays_count)
    _ = leaderboard_collection.insert_one(all_wins)
    _ = leaderboard_collection.insert_one(all_avg)
    _ = leaderboard_collection.insert_one(all_winnings)
    _ = leaderboard_collection.insert_one(all_overall)

### flass.py

from flask import Flask
from flask import request
import pyautogui as pg
import os
import time
import subprocess
from PIL import ImageGrab
import re
import os.path
import sys
import base64
import requests
import xmltodict
pg.FAILSAFE = False
pattern = r'^[a-zA-Z][0-9]{7}$'

app = Flask(__name__)

@app.route('/addtodist', methods=['GET','POST'])
def add_user():
    data = request.json
    username = data['username']
    command = f'powershell C:\\amit\\adduser.ps1 {username} "wordle"'
    message = int(os.popen(f'cmd /c {command}').read())
    if message == 1:
        print(f'added {username} to distribution!')
        return 'success'
    return 'failure'
"""
@app.route('/addnewuser', methods=['GET','POST'])
def add_photo():
    def press1():
        time.sleep(3)
        pg.press('tab')
        pg.press('enter')
        print(f'added {username} photo!')
    data = request.json
    username = data['username']
    file_path = f'\\\\hmpublicvfs\\Software\\amitt\\{username}.png'
    if not os.path.exists(file_path) and re.match(pattern, username):
        pro = subprocess.Popen(f'C:\\amit\\arik.exe {username}')
        press1()
        img = ImageGrab.grabclipboard()
        img.save(f'\\\\hmpublicvfs\\Software\\amitt\\{username}.png')
        pro.terminate()
    return 'ok'
"""
@app.route('/adduserphoto', methods=['GET','POST'])
def add_photo2():
    data = request.json
    username = data['username']
    file_path = f'\\\\hmpublicvfs\\Software\\amitt\\{username}.png'
    if os.path.exists(file_path) or not re.match(pattern, username):
        print(f'No need to add {username}')
        return 'ok'
    content = f"""<?xml
                    version="1.0"
                    encoding="utf-8"
                ?>
                <soap:Envelope
                    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/"
                    xmlns:tns="http://ws/leshem/tmunot"
                    xmlns:types="http://ws/leshem/tmunot/encodedTypes"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                    <soap:Body
                        soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                        <tns:getTmuna>
                            <misparIshi
                                xsi:type="xsd:int">
                                    {username[1:8]}
                            </misparIshi>
                        </tns:getTmuna>
                    </soap:Body>
                </soap:Envelope>"""
    headers = {'SOAPAction': ''}
    url = "http://www.jws.leshem.idf/Tmunot/services/TmunotService"
    response = requests.post(url, data=content, headers=headers)

    dict_response = xmltodict.parse(response.content)
    photo = dict_response['soapenv:Envelope']['soapenv:Body']['ns1:getTmunaResponse']['getTmunaReturn']['#text']
    with open(f'\\\\hmpublicvfs\\Software\\amitt\\{username}.png', 'wb') as fh:
        fh.write(base64.decodebytes(bytes(photo, 'utf-8')))
    print(f'Added {username} photo')
    return 'ok'

if __name__ == '__main__':
    #with open('C:\\amit\\logs\\flask.txt', 'w') as sys.stderr, open('C:\\amit\\logs\\output.txt', 'w') as sys.stdout:
    app.run(host='0.0.0.0', port=8080)


### winners.py

from pymongo import MongoClient
import datetime
today = datetime.date.today()
last = datetime.date(2022, 6, 25)
green = [47,181,83]

def find_best_score(plays):
    best_score = 7
    users = []
    for play in plays:
        if play['colors'][-1] == [green for i in range(5)]:
            if len(play['guesses']) == best_score:
                users.append(play['user'])
            elif len(play['guesses']) < best_score:
                users = []
                best_score = len(play['guesses'])
                users.append(play['user'])
    return [users, best_score]
def str_to_date(str_date):
    return datetime.date(int(str_date[0:4]), int(str_date[5:7]), int(str_date[8:10]))

langEN = False
client = MongoClient('mongodb://root:wordle@mongodb:27017/')
db = client['wordle'] if langEN else client['hewordle']
winners_collection = db["winners"]

dates = []
for item in db.list_collection_names():
    if len(item) == 10:
        dates.append(item)
all_dates = sorted(dates)

if (today - str_to_date(all_dates[-1])).days == 1:
    date = all_dates[-1]
elif (today - str_to_date(all_dates[-2])).days == 1:
    date = all_dates[-2]
else:
    date = None

if date != None:
    date_collection = db[date]
    cursor = date_collection.find({})
    all_plays = []
    for play in cursor:
        all_plays.append(play)
    users, score = find_best_score(all_plays)
    if score != 7:
        data = {"users": users, "score": score, "date": date, "claimed_by": []}
        print(data)
        x = winners_collection.insert_one(data)

langEN = True
client = MongoClient('mongodb://root:wordle@mongodb:27017/')
db = client['wordle'] if langEN else client['hewordle']
winners_collection = db["winners"]

dates = []
for item in db.list_collection_names():
    if len(item) == 10:
        dates.append(item)
all_dates = sorted(dates)

if (today - str_to_date(all_dates[-1])).days == 1:
    date = all_dates[-1]
elif (today - str_to_date(all_dates[-2])).days == 1:
    date = all_dates[-2]
else:
    date = None

if date != None:
    date_collection = db[date]
    cursor = date_collection.find({})
    all_plays = []
    for play in cursor:
        all_plays.append(play)
    users, score = find_best_score(all_plays)
    if score != 7:
        data = {"users": users, "score": score, "date": date, "claimed_by": []}
        print(data)
        x = winners_collection.insert_one(data)

### hebwords.txt

