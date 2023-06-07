import paho.mqtt.client as mqtt
import sys

client = mqtt.Client()
suspended = False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("coaster1/sensors/temperature")
        client.subscribe("suspend")
    else:
        print("Failed to connect, return code: ", rc)

def on_message(client, userdata, msg):
    global suspended
    message = msg.payload.decode("utf-8")
    if msg.topic == "suspend":
        if message.split(" ")[0] == "heater1":
            if message.split(" ")[1] == "SUSPEND":
                suspended = True
                return
            elif message.split(" ")[1] == "UNSUSPEND":
                suspended = False
                return
        return

    if suspended is False and message.split("|")[1] != " SUSPENDED":
        if int(message.split("|")[1]) < 15:
            client.publish("coaster1/actuators/heater", sys.argv[2] + " | ON")
        else:
            client.publish("coaster1/actuators/heater", sys.argv[2] + " | OFF")
    elif suspended is True:
        client.publish("coaster1/actuators/heater", sys.argv[2] + " | SUSPENDED")
    elif message.split("|")[1] == " SUSPENDED":
        client.publish("coaster1/actuators/heater", sys.argv[2] + " | TEMPERATURE SENSOR SUSPENDED")



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