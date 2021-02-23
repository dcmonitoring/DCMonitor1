# import main Flask class and request object
from flask import Flask, request, render_template


rooms = {"MM": {"temp": "", "timestamp": "", "color": ""}, "Labs": {"temp": "", "timestamp": "", "color": ""}}

# create the Flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def update_data():
    global rooms
    if request.method == 'POST':
        request_data = request.get_json()
        
        ##computer_room = request_data['computer_room']
        rooms[request_data['computer_room']]["temp"] = request_data['temp']
        rooms[request_data['computer_room']]["timestamp"] = request_data['timestamp']
        rooms[request_data['computer_room']]["color"] = request_data['color']

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