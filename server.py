# import main Flask class and request object
from flask import Flask, request, render_template
import requests
# create the Flask app
app = Flask(__name__)

TEMP_THRESHOLD = "25"
"""TELEGRAM_BOT_TOKEN = '1114209977:AAFJg8EbEXg43DRPAC6xg8_mf07sxu2ks8Q'
CHAT_ID = "gimelm"""

rooms = {"MM": {"temp": "", "timestamp": "", "color": ""}, "Labs": {"temp": "", "timestamp": "", "color": ""}}

"""#notifies telegram on high temps in computer rooms
def notify_telegram(computer_room, temp):
    requests.get("https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendmessage?chat_id=@" + CHAT_ID + "&text=Alert! Temperature is too high:\r\n " + computer_room + ": " + temp)
    #print("HIGH TEMP in " + computer_room + ": " + high_temps)"""

@app.route('/', methods=['GET', 'POST'])
def update_data():
    global rooms
    if request.method == 'POST':
        request_data = request.get_json()
        
        rooms[request_data['computer_room']]["temp"] = request_data['temp']
        rooms[request_data['computer_room']]["timestamp"] = request_data['timestamp']
        #rooms[request_data['computer_room']]["color"] = request_data['color']

        for computer_room in rooms:
            if rooms[computer_room]["temp"] < TEMP_THRESHOLD:
                rooms[computer_room]["color"] = "bg-success"
            else:
               rooms[computer_room]["color"] = "bg-danger"
               #notify_telegram(computer_room, rooms[computer_room]["temp"])  

        print(rooms)

        return "200 - OK"
    
    else:
        return render_template('chiller.html',
                            Labs_temp=rooms["Labs"]["temp"],
                            Labs_timestamp=rooms["Labs"]["timestamp"],
                            Labs_color=rooms["Labs"]["color"],
                            MM_temp=rooms["MM"]["temp"],
                            MM_timestamp=rooms["MM"]["timestamp"],
                            MM_color=rooms["MM"]["color"]
                            )                 