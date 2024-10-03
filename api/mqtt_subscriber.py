import random
import json
from paho.mqtt import client as mqtt_client
from threading import Thread

broker = 'hutpi.local'
port = 1883
topic = "/fridge/temp-humidity"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'

from .smartclock_db_operator import insertFridgeRecord
FRIDGE_TAG = 'Home'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        msg_topic = msg.topic
        msg_content = msg.payload.decode()
        if msg_topic == '/fridge/temp-humidity':
            info = json.loads(msg_content)
            # tag, temperature, humidity
            param = {
                "tag": FRIDGE_TAG,
                "temperature": info['temperature'],
                "humidity": info['humidity']}
            insertFridgeRecord((FRIDGE_TAG, info['temperature'], info['humidity']))
            print(f"fridge param: `{param}`")
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    # client.loop_forever()
    client.loop_start()
def start_listening_mqtt():
    run()
    # thread = Thread(target=run, args=())
    # thread.start()
    # thread.join()

if __name__ == '__main__':
    run()