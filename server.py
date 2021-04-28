# import main Flask class and request object
from flask import Flask, request, render_template
import requests
# create the Flask app
app = Flask(__name__)

TEMP_THRESHOLD = 25
TELEGRAM_BOT_TOKEN = '1114209977:AAFJg8EbEXg43DRPAC6xg8_mf07sxu2ks8Q'
CHAT_ID = "gimelm"

class Room:
    def __init__(self,Name="undefined",Temps=[],Timestamp="undefined",Color="unknown"):
        self.name=Name
        self.temps = Temps
        self.timestamp = Timestamp
        self.color = Color

rooms = {
    "Gimel": Room(),
    "Labs": Room(),
    "Black-Messer": Room(),
    "Sivan": Room(),
}

#rooms = {
#    "Gimel": {
#        "temp": [], "timestamp": "", "color": ""}, "Labs": {"temp": ["", ""], "timestamp": "", "color": ""}, "Messer": {"temp": ["", ""], "timestamp": "", "color": ""}}

#notifies telegram on high temps in computer rooms
def notify_telegram(computer_room, temps):
    temp_str = ""
    i = 1
    for temp in temps:
        temp_str += "Sensor" + str(i) + ": " + str(temp) + "\r\n"
        i += 1

    requests.get("https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendmessage?chat_id=@" + CHAT_ID + "&text=Alert! Temperature in " + computer_room + " is too high:\r\n " + temp_str)

@app.route('/', methods=['GET', 'POST'])
def update_data():
    global rooms
    if request.method == 'POST':
        request_data = request.get_json()
        computer_room = request_data['computer_room']
        
        rooms[computer_room].name = computer_room
        rooms[computer_room].temps = [int(te) for te in request_data['temp']]
        rooms[computer_room].timestamp = request_data['timestamp']

        if any(temp > TEMP_THRESHOLD for temp in rooms[computer_room].temps):
            rooms[computer_room].color = "red"
            notify_telegram(computer_room, rooms[computer_room].temps)
        else:
            rooms[computer_room].color = "green"

        print(rooms)

        return "200 - OK"
    
    else:
        thresholds = {
            "TEMP_COLD_THRESHOLD": 14,
            "TEMP_MID_COLD_THRESHOLD": 18,
            "TEMP_MID_HOT_THRESHOLD": 25,
            "TEMP_HOT_THRESHOLD": 28,
        }
        return render_template("chiller2.html", rooms=rooms,ts=thresholds)
        """
        return render_template('chiller.html',
                            Labs_temp1=rooms["Labs"]["temp"][0],
                            Labs_temp2=rooms["Labs"]["temp"][1],
                            Labs_timestamp=rooms["Labs"]["timestamp"],
                            Labs_color=rooms["Labs"]["color"],
                            Messer_temp1=rooms["Messer"]["temp"][0],
                            Messer_temp2=rooms["Messer"]["temp"][1],
                            Messer_timestamp=rooms["Messer"]["timestamp"],
                            Messer_color=rooms["Messer"]["color"],
                            Gimel_temp1=rooms["Gimel"]["temp"][0],
                            Gimel_temp2=rooms["Gimel"]["temp"][1],
                            Gimel_temp3=rooms["Gimel"]["temp"][2],
                            Gimel_timestamp=rooms["Gimel"]["timestamp"],
                            Gimel_color=rooms["Gimel"]["color"]
                            )
                            """
       
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
