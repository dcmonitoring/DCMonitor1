import requests

r = requests.post('http://127.0.0.1:5000/', json={"computer_room" : "Labs",
                                                    "temp" : "2888",
                                                    "timestamp" : "IT WORKED!!!",
                                                 })
r.status_code