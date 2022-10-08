import requests
import datetime
import time

def print_message(message):
    beauty_time = datetime.datetime.fromtimestamp(message['time'])
    beauty_time = beauty_time.strftime('%Y/%m/%d %H:%M')
    print(beauty_time, message['name'])
    print(message['text'])
    print()

after = 0

while True:
    response = requests.get('http://127.0.0.1:5000/messages',
                            params={'after' : after})
    response_data = response.json() #{'messages' : messages}

    for message in response_data['messages']:
        print_message(message)
        after = message['time']

    time.sleep(1)
