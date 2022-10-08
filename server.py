
import datetime
import time
from flask import Flask, request, abort
import json

app = Flask(__name__)


db = [
    {
        'name': 'Jack',
        'text': 'Привет всем!',
        'time': time.time()
    }, {
        'name': 'Mary',
        'text': 'Привет, Jack',
        'time': time.time()
    }
]

@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/status")
def status():
    server_info = {
        'status' : True,
        'time' : datetime.datetime.now().replace(microsecond=0)
            .isoformat().replace("T"," "),
        'name' : "katerok",
        'msg_num' : len(db),
        'usr_num' : len(set(msg['name'] for msg in db))
    }
    return server_info

@app.route("/send", methods=['POST'])
def send_message():
    if not isinstance(request.json, dict):
        return abort(400)

    name = request.json['name']
    text = request.json['text']

    userstats = {}
    if text == '/userstats':
        for message in db:
            if message['name'] in userstats.keys():
                userstats[message['name']] = userstats[message['name']] + 1
            else:
                userstats[message['name']] = 1
        db.append({ 'name': 'BOT',
                    'text': json.dumps(userstats)
                    })
        return {'ok', True}


    if not (isinstance(name, str)
        and isinstance(text, str)
           and name
           and text):
        return abort(400)

    new_message = {
        'name' : name,
        'text' : text,
        'time' : time.time()
    }
    db.append(new_message)
    return {'ok', True}

@app.route("/messages")
def get_messages():
    try:
        after = float(request.args.get('after', 0))
    except ValueError:
        return abort(400)

    messages = []
    for message in db:
        if message['time']>after:
            messages.append(message)
    return {'messages' : messages}

app.run()
