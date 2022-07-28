import loop_main
import time
import keyboard

buttons = ['a', 's', 'd', 'r', 'f', 't', 'z', 'u', 'j', 'i','k', 'l', 'ö']

class manual_manager():
    def __init__(self, light_list: list):
        self.lights = light_list

    def run_manual(self):
        try:
            for button in buttons:
                if keyboard.is_pressed(button):
                    self.lights[buttons.index(button)].turn_on()
                else:
                    self.lights[buttons.index(button)].turn_off()
        except Exception:
            pass


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
