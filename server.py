# import main Flask class and request object
from flask import Flask, request, render_template
import requests
# create the Flask app
app = Flask(__name__)

TEMP_THRESHOLD = "25"

rooms = {"MM": {"temp": "", "timestamp": "", "color": ""}, "Labs": {"temp": "", "timestamp": "", "color": ""}}

@app.route('/', methods=['GET', 'POST'])
def update_data():
    global rooms
    if request.method == 'POST':
        request_data = request.get_json()
        
        rooms[request_data['computer_room']]["temp"] = request_data['temp']
        rooms[request_data['computer_room']]["timestamp"] = request_data['timestamp']

        for computer_room in rooms:
            if rooms[computer_room]["temp"] < TEMP_THRESHOLD:
                rooms[computer_room]["color"] = "bg-success"
            else:
               rooms[computer_room]["color"] = "bg-danger"

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