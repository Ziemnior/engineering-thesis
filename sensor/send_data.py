import paho.mqtt.client as mqtt
from read_card import RFIDReader
from sensor_id import get_sensor_id 
import time
import json


BROKER = "10.10.10.1"
PORT = 1883
SUBSCRIBED_TOPIC = 'settings'
PUBLISHING_TOPIC = str('sensor/' + get_sensor_id())


def on_connect(client, userdata, flags, result_code):
    print("Result code: " + str(result_code) + "Connected flags: " + str(flags))
    client.subscribe(SUBSCRIBED_TOPIC)
    print("Subscribed to: " + SUBSCRIBED_TOPIC)
    client.connected_flag = True


def on_disconnect(client, userdata, flags, result_code):
    print("Disconnected with result code: " + str(result_code))
    client.connected_flag = False


def on_message(client, userdata, msg):
    print(msg.topic + ": " + str(msg.payload.decode("utf-8")))


def on_publish(client, userdata, mid):
    print("mid: " + str(mid))


def on_log(client, userdata, level, buf):
    print(str(level) + ": " + buf)


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_log = on_log

    try:
        client.connect(BROKER, PORT, 60)
    except:
        print("Connection error")

    client.loop_start()
    reader = RFIDReader()

    while True:
        card_readings = reader.read_card()
        client.publish(PUBLISHING_TOPIC, card_readings)
        time.sleep(3)
