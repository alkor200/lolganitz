import random
import sys
import time

from collections import deque

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

relais = [26, 16, 20, 21, 5, 6, 13, 19, 17, 18, 27, 22, 23, 24, 25, 12]


class Light:

    def __init__(self, number: int, pin: int):
        self.number = number
        self.pin = pin
        self.state = False
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def evaluate(self):
        if self.state:
            GPIO.setup(self.pin, GPIO.HIGH)
            print("on")
        else:
            GPIO.setup(self.pin, GPIO.LOW)
            print("off")

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def toggle_state(self):
        self.state = not self.state


class LightManager:

    def __init__(self, light_list: list):
        self.lights = light_list

    def run_in_row(self):
        for light in light_list:
            print(light.number)
            light.turn_on()
            time.sleep(0.1)
            light.turn_off()

    def all_on(self):
        for light in light_list:
            light.turn_on()

    def all_off(self):
        for light in light_list:
            light.turn_off()

    def action_1(self):
        self.all_on()
        time.sleep(3)
        self.all_off()
        self.run_in_row()
        self.all_on()
        time.sleep(1)
        self.all_off()
        time.sleep(1)

    def action_2(self):
        for i, light in enumerate(self.lights):
            light.turn_on()
            self.lights[len(self.lights) - i - 1].turn_on()
            time.sleep(0.2)
            light.turn_off()
            self.lights[len(self.lights) - i - 1].turn_off()

    def check_unique_lights(self, light_indices):
        return len(set(light_indices))

    def random_lights(self, sleep_time, light_count):
        old_indices = None
        while True:
            light_indices = deque(maxlen=light_count)
            for i in range(light_count):
                while True:
                    index = random.randint(0, len(self.lights) - 1)
                    light_indices.append(index)
                    if self.check_unique_lights(list(light_indices)) == light_count:
                        if list(light_indices) != old_indices:
                            old_indices = list(light_indices)
                            break

            for index in light_indices:
                self.lights[index].turn_on()

            time.sleep(sleep_time)

            for index in light_indices:
                self.lights[index].turn_off()


if __name__ == '__main__':
    light_list = []
    i = 0
    for pin in relais:
        light_list.append(
            Light(number=i, pin=pin)
        )
        i += 1
    light_manager = LightManager(light_list)
    while True:
        try:
            light_manager.random_lights(1, 1)
        except KeyboardInterrupt:
            light_manager.all_off()
            sys.exit(0)
