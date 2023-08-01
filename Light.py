import RPi.GPIO as GPIO

from abc import ABC, abstractmethod

import mcp23017 as m


class Light(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def turn_on(self):
        pass

class MCPLight(Light):
    def __init__(self, mcp, port, number: int, pin):
        self.mcp = mcp
        self.port = port
        self.pin = pin
        self.number = number

    def turn_off(self):
        self.mcp.set_gpio_pin(self.port, self.pin, m.LOW)

    def turn_on(self):
        self.mcp.set_gpio_pin(self.port, self.pin, m.HIGH)

class StandardLight(Light):
    def __init__(self, number: int, pin: int):
        self.number = number
        self.pin = pin
        self.state = False
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)
