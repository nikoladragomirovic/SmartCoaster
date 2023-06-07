import paho.mqtt.client as mqtt
import time
import sys
import random

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        pass
    else:
        print("Failed to connect, return code: ", rc)

client.on_connect = on_connect

broker_address = sys.argv[1]
port = 1883
client.connect(broker_address, port=port)

client.loop_start()

topic = "coaster1/sensors/weight"

while True:
    message = sys.argv[2] + " | " + str(random.randint(0,10))
    client.publish(topic, message)
    try:
        time.sleep(2)
    except:
        pass