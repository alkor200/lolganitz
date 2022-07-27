import time
import sys

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

relais = [26, 16, 20, 21, 5, 6, 13, 19, 17, 18, 27, 22, 23, 24, 25, 12]

def init():
    for pin in relais:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

def switch_on(relais_pin, on_time):
    try:
        GPIO.output(relais_pin, GPIO.HIGH)
        time.sleep(on_time)
        GPIO.output(relais_pin, GPIO.LOW)
    except KeyboardInterrupt:
        GPIO.output(relais_pin, GPIO.LOW)
        sys.exit(0)


if __name__ == '__main__':
    init()

    while True:
        for pin in relais:
            switch_on(pin, 0.2)
