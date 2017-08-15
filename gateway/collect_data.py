import paho.mqtt.client as mqtt
from optparse import OptionParser
import time
import json
import requests


BROKER = "10.10.10.1"
PORT = 1883
SUBSCRIBED_TOPIC = '#'


def on_connect(client, userdata, flags, result_code):
    print("Result code: " + str(result_code) + "Connected flags: " + str(flags))
    client.subscribe(SUBSCRIBED_TOPIC)
    print("Subscribed to: " + SUBSCRIBED_TOPIC)
    client.connected_flag = True


def on_disconnect(client, userdata, flags, result_code):
    print("Disconnected with result code: " + str(result_code))
    client.connected_flag = False


def on_message(client, userdata, msg):
    print(msg.topic + " " + msg.payload)
    msg_to_send = json.dumps(msg.payload.decode("utf-8"))
    #r = requests.post('http://10.10.10.1', data=msg_to_send)


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

    while True:
	time.sleep(1)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-u', '--url', dest='url', help='Please specify gateway address')
    options, args = parser.parse_args()
    
    main()
