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
    def run_in_row(self, reverse=False, interval=0.2):
        if not reverse:
            for light in self.lights:
                light.turn_on()
                time.sleep(interval)
                light.turn_off()
        else:
            for i in range(len(self.lights)):
                light_list[len(self.lights) - 1 - i].turn_on()
                time.sleep(interval)
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
            time.sleep(0.2)
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
        self.lights[middle].turn_off()
        time.sleep(0.2)
        self.lights[middle].turn_on()
        for i in range(middle):
            self.lights[middle - i - 1].turn_off()
            self.lights[middle + i + 1].turn_off()
            time.sleep(0.2)
            self.lights[middle - i - 1].turn_on()
            self.lights[middle + i + 1].turn_on()

    def action_5(self, interval=0.5):
        for i in range(int(len(self.lights) / 2)):
            self.lights[i].turn_on()
            self.lights[len(self.lights) - i - 1].turn_on()
            time.sleep(interval)
        self.lights[6].turn_on()
        time.sleep(interval)
        for i in range(int(len(self.lights) / 2)):
            self.lights[i].turn_off()
            self.lights[len(self.lights) - i - 1].turn_off()
            time.sleep(interval)
        self.lights[6].turn_off()
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
            time.sleep(0.2)
        self.lights[12].turn_off()
        time.sleep(0.2)

    def action_7(self, interval=0.2):
        for i in range(int(len(self.lights) / 2)):
            self.lights[i].turn_on()
            self.lights[len(self.lights) - i - 1].turn_on()
            time.sleep(interval)
        mid = int(len(self.lights) / 2) - 1
        self.lights[6].turn_on()
        time.sleep(interval)
        self.lights[6].turn_off()
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

    def up_down(self, upper_lights=[1, 2, 4, 7, 8, 10],
                lower_lights=[0, 3, 5, 9, 11, 12], interval=0.4):
        for i in range(2, 15):

            for light in upper_lights:
                self.lights[light].turn_on()

            time.sleep(2 / i)
            for light in upper_lights:
                self.lights[light].turn_off()

            for light in lower_lights:
                self.lights[light].turn_on()

            time.sleep(2 / i)
            for light in lower_lights:
                self.lights[light].turn_off()
        for i in range(2, 15)[::-1]:

            for light in upper_lights:
                self.lights[light].turn_on()

            time.sleep(2 / i)
            for light in upper_lights:
                self.lights[light].turn_off()

            for light in lower_lights:
                self.lights[light].turn_on()

            time.sleep(2 / i)
            for light in lower_lights:
                self.lights[light].turn_off()

    def parable_lights(self):
        for light in self.lights:
            x = light.number
            on_time = (0.342 * (x - 6.5) ** 2 + 3.919) / 25
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
            on_time = (0.342 * (x - 6.5) ** 2 + 3.919) / 30
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

    def bounce(self, interval=0.15):
        lights = [0, 1, 2, 3, 5, 6, 7, 9, 10, 11]
        for light in lights:
            self.lights[light].turn_on()
            time.sleep(interval)
            self.lights[light].turn_off()
        for light in lights[::-1]:
            self.lights[light].turn_on()
            time.sleep(interval)
            self.lights[light].turn_off()

    def circle_switch(self, interval=1):
        circle_1 = [0, 1, 2, 3]
        circle_2 = [5, 6, 7, 8, 10]
        circles = [circle_1, circle_2]

        for circle in circles:
            for light in circle:
                self.lights[light].turn_on()
            time.sleep(interval)
            for light in circle:
                self.lights[light].turn_off()

    def left_circle_fill(self, interval=0.2):
        circle_1 = [0, 1, 2, 3]

        for light in circle_1:
            self.lights[light].turn_on()
            time.sleep(interval)
        for light in circle_1:
            self.lights[light].turn_off()
            time.sleep(interval)

    def right_circle_fill(self, interval=0.2):
        circle_2 = [5, 6, 7, 8, 10]

        for light in circle_2:
            self.lights[light].turn_on()
            time.sleep(interval)
        for light in circle_2:
            self.lights[light].turn_off()
            time.sleep(interval)

    def both_circle_fill(self, interval=0.4):
        circle_1 = [0, 1, 2, 3]
        circle_2 = [5, 6, 7, 8, 10]
        circles = [circle_1, circle_2]

        for circle in circles:
            for light in circle:
                self.lights[light].turn_on()
                time.sleep(interval)
            for light in circle:
                self.lights[light].turn_off()

    def switch_small_big(self, interval=0.4):
        small = [0,2,3,4,6,8,10,11]
        big = [1,5,7,9,12]

        all = [small, big]

        for lights in all:
            for light in lights:
                self.lights[light].turn_on()
            time.sleep(interval)
            for light in lights:
                self.lights[light].turn_off()

    def start_up(self):
        self.all_on()
        time.sleep(2)
        for i in range(10):
            self.strobe(interval=0.15)
        self.all_on()
        time.sleep(1)
        self.run_in_row(interval=0.4)
        self.run_in_row(interval=0.4, reverse=True)
        self.run_in_row(interval=0.2)
        self.run_in_row(interval=0.2, reverse=True)
        self.all_on()
        time.sleep(2)
        self.all_off()
        time.sleep(2)
        for i in range(3):
            self.action_7()
        time.sleep(2)
        for i in range(10):
            self.strobe(interval=0.15)

    def focus_on_the_ball(self):
        time.sleep(60)

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
        light_manager.around_the_clock,
        light_manager.bounce,
        light_manager.left_circle_fill,
        light_manager.right_circle_fill,
        light_manager.both_circle_fill,
        light_manager.switch_small_big,
        light_manager.focus_on_the_ball,
        light_manager.focus_on_the_ball,
        light_manager.focus_on_the_ball,
    ]
    while True:
        try:
            """
            runtime = random.randint(30, 50)
            start = time.time()
            effect = random.choice(effects)
            while later - start < runtime:
                print(effect.__name__)
                effect()
                light_manager.all_off()
                later = time.time()
            """
            #light_manager.switch_small_big()
            #light_manager.run_in_row(interval=0.02)
            light_manager.right_circle_fill(0.02)
        except KeyboardInterrupt:
            light_manager.all_off()
            sys.exit(0)
        except Exception as e:
            print(e)
            light_manager.all_off()
            pass
