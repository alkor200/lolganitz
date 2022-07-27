import random
import sys
import time

from collections import deque

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

relais = [26, 16, 20, 21, 5, 6, 19, 13, 18, 17, 27, 23, 22]  # , 24, 25, 12]


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

    ### UTILS ####

    def all_on(self):
        for light in light_list:
            light.turn_on()

    def all_off(self):
        for light in light_list:
            light.turn_off()

    def check_unique_lights(self, light_indices):
        return len(set(light_indices))

    ### EFFECTS ####
    def run_in_row(self, reverse=False, interval=0.25):
        if not reverse:
            for light in self.lights:
                light.turn_on()
                time.sleep(interval)
                light.turn_off()
        else:
            for i in range(len(self.lights)):
                light_list[len(self.lights) - 1 - i].turn_on()
                time.sleep(0.1)
                light_list[len(self.lights) - 1 - i].turn_off()

    def multiple_run_in_row(self, interval=0.3):
        offset = 4
        for i, light in enumerate(self.lights):
            light.turn_on()
            self.lights[(i + offset) % len(self.lights)].turn_on()
            self.lights[(i + 2 * offset) % len(self.lights)].turn_on()
            self.lights[(i + 3 * offset) % len(self.lights)].turn_on()

            time.sleep(interval)
            light.turn_off()
            self.lights[(i + offset) % len(self.lights)].turn_off()
            self.lights[(i + 2 * offset) % len(self.lights)].turn_off()
            self.lights[(i + 3 * offset) % len(self.lights)].turn_off()


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
            time.sleep(0.1)
            light.turn_off()
            self.lights[len(self.lights) - i - 1].turn_off()

    def action_3(self):
        self.run_in_row()
        self.action_2()
        self.run_in_row(reverse=True)

    def ping_pong(self):
        j = 0
        step = True
        first = True
        middle = int(len(self.lights) / 2 - 1) + 1
        for i in range(2 * len(self.lights)):
            if step:
                index = (middle + j) % len(self.lights)
            else:
                index = (middle - j) % len(self.lights)
            if first:
                first = False
                step = False
            if not step:
                step = True
            else:
                j += 1
                step = False
            self.lights[index].turn_on()
            time.sleep(0.3)
            self.lights[index].turn_off()

    def ping_pong_inverted(self):
        middle = int(len(self.lights) / 2 - 1) + 1
        j = 0
        first = True
        step = True
        for i in range(2 * len(self.lights)):
            if step:
                index = (middle + j) % len(self.lights)
            else:
                index = (middle - j) % len(self.lights)
            if first:
                first = False
                step = False
            if not step:
                step = True
            else:
                j += 1
                step = False
            for light in self.lights:
                if light.number != index:
                    light.turn_on()
            time.sleep(0.3)
            for light in self.lights:
                light.turn_off()

    def action_4(self):
        middle = int(len(self.lights) / 2)
        for light in self.lights:
            light.turn_on()
        for i in range(middle):
            self.lights[middle - 1 - i].turn_off()
            self.lights[middle + i].turn_off()
            time.sleep(0.1)
            self.lights[middle - 1 - i].turn_on()
            self.lights[middle + i].turn_on()
        time.sleep(0.3)

    def action_5(self, interval=0.5):
        for i in range(int(len(self.lights) / 2)):
            self.lights[i].turn_on()
            self.lights[len(self.lights) - i - 1].turn_on()
            time.sleep(interval)
        for i in range(int(len(self.lights) / 2)):
            self.lights[i].turn_off()
            self.lights[len(self.lights) - i - 1].turn_off()
            time.sleep(interval)

    def action_6(self):
        middle = int(len(self.lights) / 2 - 1) + 1
        i = 0
        first = True
        step = True
        reverse = False
        count = 0
        for j in range(2 * len(self.lights) + 1):
            if step:
                index = (middle + i) % len(self.lights)
            else:
                index = (middle - i) % len(self.lights)
            if first:
                # i += 1
                first = False
                step = False
            if not step:
                step = True
            else:
                i += 1
                step = False
            if not reverse:
                self.lights[index].turn_on()
            else:
                self.lights[index].turn_off()
            if count < len(self.lights):
                count += 1
            else:
                count = 0
                i = 0
                reverse = not reverse
            time.sleep(0.3)

    def action_7(self, interval=0.3):
        for i in range(int(len(self.lights) / 2)):
            self.lights[i].turn_on()
            self.lights[len(self.lights) - i - 1].turn_on()
            time.sleep(interval)
        mid = int(len(self.lights) / 2) - 1
        for i in range(int(len(self.lights) / 2)):
            self.lights[mid - i].turn_off()
            self.lights[mid + i + 1].turn_off()
            time.sleep(interval)
        self.lights[0].turn_off()
        self.lights[len(self.lights) - 1].turn_off()
        time.sleep(2 * interval)

    def random_lights(self, sleep_time=0.2, light_count=3):
        old_indices = None
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

    def flicker(self):
        print("ficker")
        for light in self.lights:
            light.turn_on()

        off_lights = random.choices(self.lights, k=random.randint(1, 8))

        for light in off_lights:
            light.turn_off()
        time.sleep(0.2)

    def every_second_light(self):
        second = False
        for light in self.lights:
            if second:
                light.turn_on()
                second = False
            else:
                light.turn_off()
                second = True

        time.sleep(1)
        for light in self.lights:
            light.turn_off()
        second = False
        for light in self.lights:
            if second:
                light.turn_off()
                second = False
            else:
                light.turn_on()
                second = True

        time.sleep(1)
        for light in self.lights:
            light.turn_off()


    def all_on(self):
        for light in self.lights:
            light.turn_on()

    def strobe(self, interval=0.07):
        for light in self.lights:
            light.turn_on()

        time.sleep(interval)
        for light in self.lights:
            light.turn_off()

        time.sleep(interval)

    def action_strobe(self):
        for i in range(20):
            self.strobe()
        time.sleep(3)

    def up_down(self, upper_lights=[1, 3, 5, 7], lower_lights=[2, 4, 6, 8], interval=0.4):
        for light in upper_lights:
            self.lights[light].turn_on()

        time.sleep(interval)
        for light in upper_lights:
            self.lights[light].turn_off()

        for light in lower_lights:
            self.lights[light].turn_on()

        time.sleep(interval)
        for light in lower_lights:
            self.lights[light].turn_off()

    def parable_lights(self):
        for light in self.lights:
            x = light.number
            on_time = (0.342 * (x - 8) ** 2 + 3.919) / 25
            light.turn_on()
            try:
                if not x == 0:
                    self.lights[x - 1].turn_on()
            except:
                pass
            try:
                self.lights[x + 1].turn_on()
            except:
                pass

            time.sleep(on_time)
            self.all_off()

        for light in self.lights[::-1][1:-1]:
            x = light.number
            on_time = (0.342 * (x - 8) ** 2 + 3.919) / 25
            light.turn_on()
            try:
                if not x == 0:
                    self.lights[x - 1].turn_on()
            except:
                pass
            try:
                self.lights[x + 1].turn_on()
            except:
                pass

            time.sleep(on_time)
            self.all_off()

    def around_the_clock(self,
                         upper_lights=[0, 1, 2, 4, 7, 8, 10, 12, 11],
                         lower_lights=[3, 5, 6, 9],
                         interval=0.15):
        for light in upper_lights:
            self.lights[light].turn_on()

            time.sleep(interval)
            self.all_off()

        for light in lower_lights[::-1]:
            self.lights[light].turn_on()

            time.sleep(interval)
            self.all_off()


if __name__ == '__main__':
    light_list = []
    i = 0
    light_manager = LightManager(light_list)
    for pin in relais:
        light_list.append(
            Light(number=i, pin=pin)
        )
        i += 1
    later = time.time()

    effects = [
        light_manager.random_lights,
        light_manager.ping_pong,
        light_manager.flicker,
        light_manager.action_strobe,
        light_manager.run_in_row,
        light_manager.multiple_run_in_row,
        light_manager.action_2,
        light_manager.action_3,
        light_manager.action_4,
        light_manager.action_5,
        light_manager.action_6,
        light_manager.action_7,
        light_manager.ping_pong_inverted,
        light_manager.every_second_light,
        light_manager.up_down,
        light_manager.parable_lights,
        light_manager.around_the_clock
    ]
    while True:
        try:
            # runtime = random.randint(20, 30)
            # start = time.time()
            # effect = random.choice(effects)
            # while later - start < runtime:
                # print(effect.__name__)
                # effect()
                # later = time.time()
            #light_manager.around_the_clock()
            light_manager.run_in_row()
        except KeyboardInterrupt:
            light_manager.all_off()
            sys.exit(0)
        except Exception as e:
            print(e)
            light_manager.all_off()
            pass
