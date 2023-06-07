import paho.mqtt.client as mqtt
import time
import sys
import random

client = mqtt.Client()
suspended = False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("suspend")
    else:
        print("Failed to connect, return code: ", rc)

def on_message(client, userdata, msg):
    global suspended
    message = msg.payload.decode("utf-8")
    if message.split(" ")[0] == "temperature1":
        if message.split(" ")[1] == "SUSPEND":
            suspended = True
            return
        elif message.split(" ")[1] == "UNSUSPEND":
            suspended = False
            return
    return

client.on_connect = on_connect
client.on_message = on_message

broker_address = sys.argv[1]
port = 1883
client.connect(broker_address, port=port)

client.loop_start()

topic = "coaster1/sensors/temperature" 

while True:
    if suspended is False:
        message = sys.argv[2] + " | " + str(random.randint(0,40))
    else:
        message = sys.argv[2] + " | SUSPENDED"
    client.publish(topic, message)
    try:
        time.sleep(2)
    except:
        pass