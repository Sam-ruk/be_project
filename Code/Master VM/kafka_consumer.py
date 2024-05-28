from confluent_kafka import Consumer
import socket
import json
import os

conf = {'bootstrap.servers': "13.200.252.163:9092",
        'group.id': "be_project",'auto.offset.reset':'earliest'}

consumer = Consumer(conf)
consumer.subscribe(['project'])

def main():
    while True:
        msg = None
        msg = consumer.poll(1.0)  # timeout
        if msg is not None:
            if msg.error():
                print('Error: {}'.format(msg.error()))

            else:
                data = msg.value().decode('utf-8')
                val = list(json.loads(data).values())

                # Formatting the data as a CSV chunk
                val = ','.join([str(x) for x in val[0:len(val)]])
                print(val)
                
                # Remove first record (line2) (display latest 50) from dashboard_data.csv, using a temp file
                os.system("sed '2d' dashboard_data.csv > dashboard_49.csv")
                os.system("mv dashboard_49.csv dashboard_data.csv")

                # Append the latest data point to dashboard_data.csv
                os.system('echo "{}" >> dashboard_data.csv'.format(val))

    consumer.close()

if __name__ == "__main__":
    main()
