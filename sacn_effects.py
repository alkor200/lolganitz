import sacn
import time
import random


def alternate_blinking(step, threshold=50):
    value1 = 255 if step % 4 < 2 else 0
    value2 = 255 if step % 4 >= 2 else 0
    print(f"Alternating Blinking effect - Group 1: {value1}, Group 2: {value2}")
    return tuple(value1 if i < 20 else value2 for i in range(40))


def wave_effect(step, threshold=50):
    index = step % 40
    values = [0] * 40
    values[index] = 255
    if index > 0:
        values[index - 1] = 255
    if index < 39:
        values[index + 1] = 255
    print(f"Wave effect at index {index}")
    return tuple(values)


def random_flash(step, threshold=50):
    values = tuple(255 if random.randint(0, 1) else 0 for _ in range(40))
    print("Random Flash effect")
    return values


def binary_chase_effect(step, threshold=50):
    index = step % 40
    print(f"Binary Chase effect at index {index}")
    return tuple(255 if i == index else 0 for i in range(40))


def strobe_effect(step, threshold=50):
    value = 255 if step % 10 < 5 else 0  # Modify this to change strobe speed
    print(f"Strobe effect with value {value}")
    return (value,) * 40


effects = [alternate_blinking, wave_effect, random_flash, binary_chase_effect, strobe_effect]

sender = sacn.sACNsender(fps=180)
sender.start()
sender.activate_output(1)
sender[1].multicast = False
sender[1].destination = "10.10.7.17"

interval = 0.2
step = 0
try:
    while True:
        current_effect = effects[step % len(effects)]
        dmx_tuple = current_effect(step)
        sender[1].dmx_data = dmx_tuple
        print(f"Sent DMX Values using effect: {current_effect.__name__}")

        step += 1
        time.sleep(interval)
except KeyboardInterrupt:
    print("Stopping sender...")
    sender.stop()
