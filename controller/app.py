from flask import Flask, render_template, request
import paho.mqtt.client as mqtt

app = Flask(__name__)

temperature_suspended = False
weight_suspended = False
led_suspended = False
heater_suspended = False

temperature_data = "NO DATA"
weight_data = "NO DATA"
led_data = "NO DATA"
heater_data = "NO DATA"

temperature_topic = "coaster1/sensors/temperature"
weight_topic = "coaster1/sensors/weight"
led_topic = "coaster1/actuators/led"
heater_topic = "coaster1/actuators/heater"

mqtt_broker = "127.0.0.1"
mqtt_port = 1883

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    for i in range(1, 3):
        client.subscribe("coaster"+str(i)+"/sensors/temperature")
        client.subscribe("coaster"+str(i)+"/sensors/weight")
        client.subscribe("coaster"+str(i)+"/actuators/led")
        client.subscribe("coaster"+str(i)+"/actuators/heater")

def on_message(client, userdata, msg):
    global temperature_data, weight_data, led_data, heater_data

    if msg.topic == temperature_topic:
        temperature_data = msg.payload.decode('utf-8')

    elif msg.topic == weight_topic:
        weight_data = msg.payload.decode('utf-8')

    elif msg.topic == led_topic:
        led_data = msg.payload.decode('utf-8')

    elif msg.topic == heater_topic:
        heater_data = msg.payload.decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temperature', methods=['GET', 'POST'])
def get_temperature():
    global temperature_suspended

    item = request.form.get('item')

    if request.method == 'POST':
        if temperature_suspended:
            temperature_suspended = False
            mqtt_client.publish("suspend", item + " UNSUSPEND")
        else:
            temperature_suspended = True
            mqtt_client.publish("suspend", item + " SUSPEND")

    return temperature_data

@app.route('/weight', methods=['GET', 'POST'])
def get_weight():
    global weight_suspended

    item = request.form.get('item')

    if request.method == 'POST':
        if weight_suspended:
            weight_suspended = False
            mqtt_client.publish("suspend", item + " SUSPEND")
        else:
            weight_suspended = True
            mqtt_client.publish("suspend", item + " UNSUSPEND")
    return weight_data

@app.route('/led', methods=['GET', 'POST'])
def get_led():
    global led_suspended

    item = request.form.get('item')

    if request.method == 'POST':
        if led_suspended:
            led_suspended = False
            mqtt_client.publish("suspend", item + " SUSPEND")
        else:
            led_suspended = True
            mqtt_client.publish("suspend", item + " UNSUSPEND")
    return led_data

@app.route('/heater', methods=['GET', 'POST'])
def get_heater():
    global heater_suspended

    item = request.form.get('item')

    if request.method == 'POST':
        if heater_suspended:
            heater_suspended = False
            mqtt_client.publish("suspend", item + " SUSPEND")
        else:
            heater_suspended = True
            mqtt_client.publish("suspend", item + " UNSUSPEND")
    return heater_data

@app.route('/topics', methods=['POST'])
def change_topics():
    global temperature_topic, weight_topic, led_topic, heater_topic
    global temperature_data, weight_data, led_data, heater_data

    selected_value = request.form.get('selectedValue')

    temperature_data = "NO DATA"
    weight_data = "NO DATA"
    led_data = "NO DATA"
    heater_data = "NO DATA"

    temperature_topic = "coaster"+selected_value.strip("C")+"/sensors/temperature"
    weight_topic = "coaster"+selected_value.strip("C")+"/sensors/weight"
    led_topic = "coaster"+selected_value.strip("C")+"/actuators/led"
    heater_topic = "coaster"+selected_value.strip("C")+"/actuators/heater"

    return 'SUCCESS'

if __name__ == '__main__':
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(mqtt_broker, mqtt_port)
    mqtt_client.loop_start()

    app.run(host='0.0.0.0', debug=True)