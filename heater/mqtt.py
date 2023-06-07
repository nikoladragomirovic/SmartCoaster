import paho.mqtt.client as mqtt
import sys

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("coaster1/sensors/temperature")
    else:
        print("Failed to connect, return code: ", rc)

def on_message(client, userdata, msg):
    message = msg.payload.decode("utf-8")
    if int(message.split("|")[1]) < 15:
        client.publish("coaster1/actuators/heater", sys.argv[2] + " | ON")
    else:
        client.publish("coaster1/actuators/heater", sys.argv[2] + " | OFF")

client.on_connect = on_connect
client.on_message = on_message

broker_address = sys.argv[1]
port = 1883
client.connect(broker_address, port=port)

client.loop_start()

try:
    while True:
        pass
except:
    pass