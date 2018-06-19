#!/usr/bin/env python

import paho.mqtt.client as mqtt
from optparse import OptionParser
from gateway_id import get_gateway_id
import time
import json
import requests
 
 
class CollectData:
    def __init__(self, url):
        self.client = mqtt.Client()
        self.broker = "10.10.10.1"
        self.port = 1883
        self.subscribed_topic = '#'
        self.url = url
 
    def on_connect(self, client, userdata, flags, result_code):
        print("Result code: " + str(result_code) + ", Connected flags: " + str(flags))
        client.subscribe(self.subscribed_topic, qos=2)
        print("Subscribed to: " + self.subscribed_topic)
 
    def on_disconnect(self, client, userdata, flags, result_code):
        print("Disconnected with result code: " + str(result_code))
 
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        msg_to_send = json.loads(msg.payload.decode("utf-8"))
	msg_to_send["gateway_id"] = get_gateway_id()
        post_message = requests.post(self.url, json=msg_to_send)
 
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
 
        try:
            client.connect(broker, port, 60)
        except ConnectionError:
            print("Connection error")
        except TimeoutError:
            print("Connection timed out")
 
        client.loop_start()
 
        while True:
            time.sleep(1)
 
 
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-u', '--url', dest='url', default='http://192.168.1.80:5000/api/post-record', help='Please specify gateway address')
    options, args = parser.parse_args()
 
    collect_data = CollectData(url=options.url)
    collect_data.main()

