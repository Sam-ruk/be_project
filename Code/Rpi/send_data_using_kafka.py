from confluent_kafka import Producer
import socket
import time
import json
import warnings
import os

warnings.filterwarnings("ignore", category=DeprecationWarning)
modification_time = os.path.getmtime('generation_data.json')

conf = {'bootstrap.servers': '13.127.39.68:9092',
        'client.id': socket.gethostname()}
producer = Producer(conf)

while True:
    print(modification_time, os.path.getmtime('generation_data.json'))
    if modification_time != os.path.getmtime('generation_data.json'):
        modification_time = os.path.getmtime('generation_data.json')
        with open('generation_data.json', 'r') as json_file:
            data = json.load(json_file)
            print(data)
        producer.produce('project', json.dumps(data).encode('utf-8'))  # Encode: convert string to bytes
    time.sleep(1)

producer.flush()
