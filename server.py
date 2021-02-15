# import main Flask class and request object
from flask import Flask, request, render_template


rooms = {"MM": {"temp": "", "timestamp": ""}, "Labs": {"temp": "", "timestamp": ""}}

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

        print(rooms)

        return "200 - OK"
    
    else:
        return render_template('chiller.html',
                            Labs_temp=rooms["Labs"]["temp"],
                            Labs_timestamp=rooms["Labs"]["timestamp"],
                            MM_temp=rooms["MM"]["temp"],
                            MM_timestamp=rooms["MM"]["timestamp"]
                            )

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)