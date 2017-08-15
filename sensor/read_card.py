from time import sleep
import RPi.GPIO as GPIO
import MFRC522
from signal import signal, SIGINT
import json
from sensor_id import get_sensor_id


class RFIDReader():
    def __init__(self):
        self.isEnabled = True
        self.rfid_reader = MFRC522.MFRC522()

    def read_card(self):
        while self.isEnabled is True:
            try:
                (error, tag_type) = self.rfid_reader.MFRC522_Request(self.rfid_reader.PICC_REQIDL)
                if not error:
                    (error, uid) = self.rfid_reader.MFRC522_Anticoll()
                    if not error:
			#identifier = 
                        self.send_json(uid)
                        sleep(3)
            except:
                print("Stopping...")
                GPIO.cleanup()
                self.isEnabled = False

    def send_json(self, rfid_identifier):
	data = {'sensor_id': get_sensor_id(),
              'user_id': rfid_identifier}
        print(json.dumps(data))

if __name__ == "__main__":
    reader = RFIDReader()
    reader.read_card()

