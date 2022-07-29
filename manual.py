import loop_main
import keyboard
import time
from getkey import getkey, keys

buttons = ['a', 's', 'd', 'f', 'r', 'g', 'h', 'u','j', 'i', 'k','l', 'o']

class manual_manager():
    def __init__(self, light_list: list):
        self.lights = light_list
        self.all_off()

    def all_off(self):
        for light in self.lights:
            light.turn_off()

    def run_manual(self):
        while True:
            try:
                key = getkey()
                if key in buttons:
                    self.lights[buttons.index(key)].turn_on()
                    time.sleep(0.1)
                self.all_off()
            except Exception as e:
               print(e) 

if __name__ == '__main__':
    light_list = []
    i = 0
    manager = manual_manager(light_list)
    for pin in loop_main.relais:
        light_list.append(
            loop_main.Light(number=i, pin=pin)
        )
        i += 1
    manager.run_manual()

