# import main Flask class and request object
from flask import Flask, request, render_template
import requests
# create the Flask app
app = Flask(__name__)

TEMP_THRESHOLD = "25"
TELEGRAM_BOT_TOKEN = '1114209977:AAFJg8EbEXg43DRPAC6xg8_mf07sxu2ks8Q'
CHAT_ID = "gimelm"

rooms = {"MM": {"temp": "", "timestamp": "", "color": ""}, "Labs": {"temp": [], "timestamp": "", "color": ""}}

#notifies telegram on high temps in computer rooms
def notify_telegram(computer_room, temps):
    i = 1
    for temp in temps:
        temps_str += "Sensor" + i + ": " + temp + "\r\n"
        i += 1

    requests.get("https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendmessage?chat_id=@" + CHAT_ID + "&text=Alert! Temperature in " + computer_room " is too high:\r\n " + temps_str)

@app.route('/', methods=['GET', 'POST'])
def update_data():
    global rooms
    if request.method == 'POST':
        request_data = request.get_json()
        computer_room = request_data['computer_room']
        
        rooms[computer_room]["temp"] = request_data['temp']
        rooms[computer_room]["timestamp"] = request_data['timestamp']

        if any(temp > TEMP_THRESHOLD for temp in rooms[computer_room]["temp"]):
            rooms[computer_room]["color"] = "bg-danger"
            notify_telegram(computer_room, rooms[computer_room]["temp"])
        else:
            rooms[computer_room]["color"] = "bg-success"

        print(rooms)

        return "200 - OK"
    
    else:
        return render_template('chiller.html',
                            Labs_temp1=rooms["Labs"]["temp"][0],
                            Labs_temp2=rooms["Labs"]["temp"][1],
                            Labs_timestamp=rooms["Labs"]["timestamp"],
                            Labs_color=rooms["Labs"]["color"],
                            MM_temp=rooms["MM"]["temp"],
                            MM_timestamp=rooms["MM"]["timestamp"],
                            MM_color=rooms["MM"]["color"]
                            )                 