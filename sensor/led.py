import RPi.GPIO as GPIO
from time import sleep

LED = 18 


def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED, GPIO.OUT)


def blink_led():
    setup_gpio()
    GPIO.output(LED, True)
    sleep(1)
    GPIO.output(LED, False)
