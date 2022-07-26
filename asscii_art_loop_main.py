import os
import sys
import time
import random

from collections import deque

# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BCM)

relais = [26, 16, 20, 21, 5, 6, 13, 19, 17, 18, 27, 22, 23, 24, 25, 12]


class Light:

    def __init__(self, number: int, pin: int):
        self.number = number
        self.pin = pin
        self.state = False
        # GPIO.setup(self.pin, GPIO.OUT)
        # GPIO.output(self.pin, GPIO.LOW)

    def evaluate(self):
        if self.state:
            # GPIO.setup(self.pin, GPIO.HIGH)
            print("on")
        else:
            # GPIO.setup(self.pin, GPIO.LOW)
            print("off")

    def turn_off(self):
        self.state = False

    def turn_on(self):
        self.state = True

    def toggle_state(self):
        self.state = not self.state


class LightManager:

    def __init__(self, light_list: list):
        self.lights = light_list
        self.current_effect = ""

    def run_in_row(self, reverse=False, interval=0.1):
        if not reverse:
            for light in self.lights:
                light.turn_on()
                self.display()
                time.sleep(interval)
                light.turn_off()
        else:
            for i in range(len(self.lights)):
                light_list[len(self.lights) - 1 - i].turn_on()
                self.display()
                time.sleep(0.1)
                light_list[len(self.lights) - 1 - i].turn_off()

    def multiple_run_in_row(self, interval=0.3):
        offset = 4
        for i, light in enumerate(self.lights):
            light.turn_on()
            self.lights[(i + offset) % len(self.lights)].turn_on()
            self.lights[(i + 2*offset) % len(self.lights)].turn_on()
            self.lights[(i + 3*offset) % len(self.lights)].turn_on()
            self.display()
            time.sleep(interval)
            light.turn_off()
            self.lights[(i + offset) % len(self.lights)].turn_off()
            self.lights[(i + 2*offset) % len(self.lights)].turn_off()
            self.lights[(i + 3*offset) % len(self.lights)].turn_off()

    def all_on(self):
        for light in light_list:
            light.turn_on()

    def all_off(self):
        for light in light_list:
            light.turn_off()

    def action_1(self):
        self.all_on()
        self.display()
        time.sleep(3)
        self.all_off()
        self.display()
        self.run_in_row()
        self.all_on()
        self.display()
        time.sleep(1)
        self.all_off()
        self.display()
        time.sleep(1)

    def action_2(self):
        for i, light in enumerate(self.lights):
            light.turn_on()
            self.lights[len(self.lights) - i - 1].turn_on()
            self.display()
            time.sleep(0.1)
            light.turn_off()
            self.lights[len(self.lights) - i - 1].turn_off()
            self.display()

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
            self.display()
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
            self.display()
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
            self.display()
            time.sleep(0.1)
            self.lights[middle - 1 - i].turn_on()
            self.lights[middle + i].turn_on()
            self.display()
        time.sleep(0.3)

    def action_5(self, interval):
        for i, light in enumerate(self.lights):
            light.turn_on()
            self.lights[len(self.lights) - i - 1].turn_on()
            self.display()
            time.sleep(interval)
            # light.turn_off()
            # self.lights[len(self.lights) - i - 1].turn_off()
        for i, light in enumerate(self.lights):
            light.turn_off()
            self.lights[len(self.lights) - i - 1].turn_off()
            self.display()
            time.sleep(interval)
            # light.turn_off()
            # self.lights[len(self.lights) - i - 1].turn_off()

    def action_6(self):
        middle = int(len(self.lights)/2 - 1) + 1
        i = 0
        first = True
        step = True
        reverse = False
        count = 0
        for j in range(2*len(self.lights)+1):
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
            self.display()
            if count < len(self.lights):
                count += 1
            else:
                count = 0
                i = 0
                reverse = not reverse
            time.sleep(0.3)
            # self.lights[index].turn_off()

    def action_7(self, interval):
        for i, light in enumerate(self.lights):
            light.turn_on()
            self.lights[len(self.lights) - i - 1].turn_on()
            self.display()
            time.sleep(interval)
        mid = int(len(self.lights)/2) - 1
        for i in range(mid):
            self.lights[mid - i].turn_off()
            self.lights[mid + i + 1].turn_off()
            self.display()
            time.sleep(interval)
        self.lights[0].turn_off()
        self.lights[len(self.lights)-1].turn_off()
        self.display()
        time.sleep(2 * interval)

    def check_unique_lights(self, light_indices):
        return len(set(light_indices))

    def random_lights(self, sleep_time=0.2, light_count=5):
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
        self.display()
        time.sleep(sleep_time)
        for index in light_indices:
            self.lights[index].turn_off()

    def flicker(self):
        print("ficker")
        for light in self.lights:
            light.turn_on()
        indices = []
        for i in range(12):
            indices.append(random.randint(0, len(self.lights) - 1))
        for index in indices:
            self.lights[index].turn_off()
            self.lights[(index + 6)%len(self.lights)].turn_off()
            self.display()
            time.sleep(0.15)
            self.lights[index].turn_on()
            self.lights[(index + 6)%len(self.lights)].turn_on()
            self.display()
        time.sleep(0.3)

    def every_second_light(self):
        second = False
        for light in self.lights:
            if second:
                light.turn_on()
                second = False
            else:
                light.turn_off()
                second = True
        self.display()
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
        self.display()
        time.sleep(1)
        for light in self.lights:
            light.turn_off()

    def strobe(self, interval=0.1):
        for light in self.lights:
            light.turn_on()
            self.display()
        time.sleep(interval)
        for light in self.lights:
            light.turn_off()
            self.display()
        time.sleep(interval)

    def up_down(self, upper_lights, lower_lights, interval):
        for light in upper_lights:
            self.lights[light].turn_on()
            self.display()
        time.sleep(interval)
        for light in upper_lights:
            self.lights[light].turn_off()
            self.display()
        for light in lower_lights:
            self.lights[light].turn_on()
            self.display()
        time.sleep(interval)
        for light in lower_lights:
            self.lights[light].turn_off()
            self.display()

    def parable_lights(self):
        for light in self.lights:
            x = light.number
            on_time = (0.342 * (x - 8) ** 2 + 3.919) / 25
            light.turn_on()
            try:
                if not x == 0:
                    self.lights[x-1].turn_on()
            except:
                pass
            try:
                self.lights[x+1].turn_on()
            except:
                pass
            self.display()
            time.sleep(on_time)
            self.all_off()
            self.display()
        for light in self.lights[::-1][1:-1]:
            x = light.number
            on_time = (0.342 * (x - 8) ** 2 + 3.919) / 25
            light.turn_on()
            try:
                if not x == 0:
                    self.lights[x-1].turn_on()
            except:
                pass
            try:
                self.lights[x+1].turn_on()
            except:
                pass
            self.display()
            time.sleep(on_time)
            self.all_off()
            self.display()

    def around_the_clock(self, upper_lights, lower_lights, interval):
        for light in upper_lights:
            self.lights[light].turn_on()
            self.display()
            time.sleep(interval)
            self.all_off()
            self.display()
        for light in lower_lights[::-1]:
            self.lights[light].turn_on()
            self.display()
            time.sleep(interval)
            self.all_off()
            self.display()


    def display(self, with_numbers=True):
        os.system('cls' if os.name == 'nt' else 'clear')
        width = os.get_terminal_size().columns
        first_char = True
        print(self.current_effect)
        for light in self.lights:
            if light.state:
                print('X', end=' ')
            else:
                print('_', end=' ')
        print()
        if with_numbers:
            print("1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6")



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
        light_manager.strobe,
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
            # light_manager.random_lights(1, 3)
            # light_manager.ping_pong()
            # light_manager.random_lights(sleep_time=0.1, light_count=14)
            # light_manager.flicker()
            # light_manager.strobe(0.5)
            # light_manager.up_down([0, 2, 4, 6, 8, 10, 12, 14], [1, 3, 5, 7, 9, 11, 13, 15], 0.3)
            # light_manager.parable_lights()
            # light_manager.around_the_clock([0, 2, 4, 6, 8, 10, 12, 14], [1, 3, 5, 7, 9, 11, 13, 15], 0.1)

            runtime = random.randint(5, 10)
            start = time.time()
            effect = random.choice(effects)
            light_manager.current_effect = effect.__name__
            while later - start < runtime:
                effect()
                later = time.time()



        except KeyboardInterrupt:
            light_manager.all_off()
            sys.exit(0)
