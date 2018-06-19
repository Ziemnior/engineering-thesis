import signal
from pirc522 import RFID

isEnabled = True
rfid_reader = RFID()
utilities = rfid_reader.util()
utilities.debug = True


def end_read_from_sensor(signal, frame):
    global isEnabled
    isEnabled = False
    rfid_reader.cleanup()
    print("Reading from sensor aborted.")
    return isEnabled


def read_card():

    read_state = signal.signal(signal.SIGINT, end_read_from_sensor)

    while isEnabled:
        try:
            rfid_reader.wait_for_tag()
            (error, data) = rfid_reader.request()

            if not error:
                (error, uid) = rfid_reader.anticoll()
                if not error:
                    print("Card ID: " + str(uid))
        except read_state is False:
            rfid_reader.cleanup()
	    quit()
