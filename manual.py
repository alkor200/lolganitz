import loop_main
import time
import keyboard

buttons = ['a', 's', 'd', 'r', 'f', 't', 'z', 'h','u', 'j', 'i','k', 'l']

class manual_manager():
    def __init__(self, light_list: list):
        self.lights = light_list

    def run_manual(self):
        while True:
            for light in self.lights:
                light.turn_on()


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
