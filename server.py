# import main Flask class and request object
from flask import Flask, request, render_template
import requests
import pytz
from datetime import datetime, timedelta
# create the Flask app
app = Flask(__name__)

TEMP_THRESHOLD = 25
TELEGRAM_BOT_TOKEN = '1114209977:AAFJg8EbEXg43DRPAC6xg8_mf07sxu2ks8Q'
CHAT_ID = "gimelm"


class Room:
    def __init__(self, Name="undefined", Temps=[], Timestamp="undefined", Color="unknown", time_message="ok"):
        self.name = Name
        self.temps = Temps
        self.timestamp = Timestamp
        self.color = Color
        self.time_message = time_message


rooms = {}


def notify_telegram_temps(computer_room, temps):
    temp_str = ""
    i = 1
    for temp in temps:
        temp_str += "Sensor" + str(i) + ": " + str(temp) + "\r\n"
        i += 1

    requests.get("https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendmessage?chat_id=@" +
                 CHAT_ID + "&text=Alert! Temperature in " + computer_room + " is too high:\r\n " + temp_str)


def notify_telegram_update(computer_room, timestamp):
    requests.get("https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendmessage?chat_id=@" + CHAT_ID +
                 "&text=Alert! The agent in " + computer_room + " didn`t send any message in more then 10 minutes.\r\n Last update in " + timestamp)


@app.route('/', methods=['GET', 'POST'])
def update_data():
    global rooms
    if request.method == 'POST':
        request_data = request.get_json()
        computer_room = request_data['computer_room']
        if computer_room not in rooms.keys():
            rooms[computer_room] = Room()
        rooms[computer_room].name = computer_room
        rooms[computer_room].temps = [float(te) for te in request_data['temp']]
        rooms[computer_room].timestamp = request_data["timestamp"]
        if any(temp > TEMP_THRESHOLD for temp in rooms[computer_room].temps):
            rooms[computer_room].color = "red"
            notify_telegram_temps(computer_room, rooms[computer_room].temps)
        else:
            rooms[computer_room].color = "green"
        for room in rooms.values():
            try:
                room_last_update = datetime.strptime(
                    room.timestamp, "%a %b %d %H:%M:%S %Y")
                time_now = datetime.now(pytz.timezone("Israel")).replace(tzinfo=None)
                time_delta = time_now - room_last_update
                if time_delta > timedelta(seconds=600):
                    rooms[room.name].color = "red"
                    rooms[room.name].time_message = "{h} Hours, {m} Minutes and {s} Seconds".format(h=str(time_delta).split(":")[0], m=str(
                        time_delta).split(":")[1], s=str(time_delta).split(":")[2].split(".")[0])
                    notify_telegram_update(
                        computer_room, rooms[room.name].timestamp)
                else:
                    rooms[computer_room].time_message = "ok"
            except Exception as excepts:
                rooms[room.name].color = "red"
                print(excepts)
                if rooms[room.name].time_message == "ok":
                    rooms[room.name].time_message = "can't compare timestamps"

        return "200 - OK"

    else:
        thresholds = {
            "TEMP_COLD_THRESHOLD": 14,
            "TEMP_MID_COLD_THRESHOLD": 18,
            "TEMP_MID_HOT_THRESHOLD": 25,
            "TEMP_HOT_THRESHOLD": 28,
        }
        return render_template("chiller2.html", rooms=rooms, ts=thresholds)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
