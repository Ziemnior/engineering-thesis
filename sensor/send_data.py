#!usr/bin/env python3

import paho.mqtt.client as mqtt
from read_card import RFIDReader
from sensor_id import get_sensor_id
from led import blink_led
from time import sleep
import json
 
 
class SendData:
    def __init__(self):
        self.client = mqtt.Client()
        self.broker = "10.10.10.1"
        self.port = 1883
        self.subscribed_topic = 'settings'
        self.publishing_topic = str('sensor/' + get_sensor_id())
 
    def on_connect(self, client, userdata, flags, result_code):
        subscribed_topic = self.subscribed_topic
        print("Result code: " + str(result_code) + "Connected flags: " + str(flags))
        client.subscribe(subscribed_topic, qos=2)
        print("Subscribed to: " + subscribed_topic)
 
    def on_disconnect(self, client, userdata, flags, result_code):
        print("Disconnected with result code: " + str(result_code))
 
    def on_message(self, client, userdata, msg):
        print(msg.topic + ": " + str(msg.payload.decode("utf-8")))
 
    def on_publish(self, client, userdata, mid):
        print("mid: " + str(mid))
 
    def on_log(self, client, userdata, level, buf):
        print(str(level) + ": " + buf)
 
    def main(self):
        client = self.client
 
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message
        client.on_publish = self.on_publish
        client.on_log = self.on_log
 
        broker = self.broker
        port = self.port
        publishing_topic = self.publishing_topic
 
        try:
            client.connect(broker, port, 60)
        except ConnectionError:
            print("Connection error")
        except TimeoutError as e:
            print("Connection timed out", e)
 
        client.loop_start()
        reader = RFIDReader()
 
        while True: 
            card_readings = reader.read_card()
	    blink_led()
            client.publish(publishing_topic, card_readings, qos=2)
 
 
if __name__ == "__main__":
    send_data = SendData()
    send_data.main()

