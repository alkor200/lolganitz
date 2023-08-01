import smbus
import time
import numpy as np
import wiringpi as wpi

# CONTROL REGISTER in Sequential mode IOCON.BANK = 0
# The following registers correspond to port A,
# +1 for registers corresponding to port B
IODIR = 0x00
IPOL = 0x02
GPINTEN = 0x04
DEFVAL = 0X06
INTCON = 0x08
IOCON = 0x0A
GPPU = 0x0C
INTF = 0x0E
INTCAP = 0x10
GPIO = 0x12
OLAT = 0x14

# state definition
INPUT = 0x01
OUTPUT = 0x00
# port definition
PORTA = 0x00
PORTB = 0x01

# pin number definition
PIN0 = 0x01
PIN1 = 0x02
PIN2 = 0x04
PIN3 = 0x08
PIN4 = 0x10
PIN5 = 0x20
PIN6 = 0x40
PIN7 = 0x80
PIN_ALL = 0xFF

ENABLE = 0x01
DISABLE = 0x00

POLARITY_REV = 0x01
POLARITY_NREV = 0x00

HIGH = 0x01
LOW = 0x00

# INTERRUPT type definition
INT_DISABLE = 0x00
INT_HIGH_LEVEL = 0x01
INT_LOW_LEVEL = 0x02
INT_CHANGE_LEVEL = 0x03

# Define whether INTA and INTB are associated
INTAB_CONJUNCTION = 0x00
INTAB_INDEPENDENT = 0x01

# Define the output type of INTA and INTB pins
INT_OD = 0x00
INT_PUSHPULL_HIGH = 0x01
INT_PUSHPULL_LOW = 0x02

# INTA/B pin wiring to Raspberry Pi 4B in wiringPi number
# INTA --> P0
# INTB --> P1
PIN_INTA = 0
PIN_INTB = 1
# Module use I2C bus,the slave device address setting:
'''
0 1 0  0 A2 A1 A0 
0 1 0  0 0  0  0    0x20
0 1 0  0 0  0  1    0x21
0 1 0  0 0  1  0    0x22
0 1 0  0 0  1  1    0x23
0 1 0  0 1  0  0    0x24
0 1 0  0 1  0  1    0x25
0 1 0  0 1  1  0    0x26
0 1 0  0 1  1  1    0x27
'''


# default slave I2C interface device is 0x27(A2=1,A1=1,A0=1)

class MCP23017():
    def __init__(self):
        self.dev_addr = 0x27  # (A2=1,A1=1,A0=1)
        self.i2c = smbus.SMBus(1)  # /dev/i2c-1
        print(self.i2c)
        wpi.wiringPiSetup()
        wpi.pinMode(PIN_INTA, wpi.INPUT)
        wpi.pullUpDnControl(PIN_INTA, wpi.PUD_UP)
        wpi.pinMode(PIN_INTB, wpi.INPUT)
        wpi.pullUpDnControl(PIN_INTB, wpi.PUD_UP)
        self.set_port_dir(PORTA, INPUT)  # set PORTA as input
        self.set_port_dir(PORTB, INPUT)  # set PORTB as input
        for addr in range(2, 22):  # set other register as default value
            self.write_reg(addr, 0x00)
        # config INTA INTB independent, output type is PUSHPULL_HIGH
        self.write_reg(IOCON, INTAB_INDEPENDENT | INT_PUSHPULL_HIGH)

    # i2c bus write register
    def write_reg(self, reg, value):
        self.i2c.write_byte_data(self.dev_addr, reg, value)

    # i2c bus read register
    def read_reg(self, reg):
        return self.i2c.read_byte_data(self.dev_addr, reg)

    # Set the input and output direction of the port
    def set_port_dir(self, port, port_dir):
        if port_dir == INPUT:
            self.write_reg(IODIR + port, 0xFF)
        elif port_dir == OUTPUT:
            self.write_reg(IODIR + port, 0x00)

    # Set the specified pin of the specified port to the input or output state
    def set_io_dir(self, port, pin, pin_dir):
        state = self.read_reg(IODIR + port)
        if pin_dir == INPUT:
            state |= pin
        elif pin_dir == OUTPUT:
            state &= ~pin
        else:
            print("dir error!")
            return
        self.write_reg(IODIR + port, state)

    # Set whether the specified pin of the specified port turns on the pull-up resistance
    def set_io_pu(self, port, pin, pu):
        state = self.read_reg(GPPU + port)
        if pu == ENABLE:
            state |= pin
        elif pu == DISABLE:
            state &= ~pin
        else:
            print("pu state error!")
            return
        self.write_reg(GPPU + port, state)

    # Set whether the specified pin of the specified port reverses the port polarity
    def set_io_polarty(self, port, pin, polarity):
        state = self.read_reg(IPOL + port)
        if polarity == ENABLE:
            state |= pin
        elif polarity == DISABLE:
            state &= ~pin
        else:
            print("polarity state error!")
            return
        self.write_reg(IPOL + port, state)

    # Set whether the interrupt function and interrupt type are enabled
    # for the specified pin of the specified port
    def set_io_int(self, port, pin, int_type):
        inten_state = self.read_reg(GPINTEN + port)
        defval_state = self.read_reg(DEFVAL + port)
        intcon_state = self.read_reg(INTCON + port)
        if int_type == INT_DISABLE:
            inten_state &= ~pin
        elif int_type == INT_HIGH_LEVEL:
            inten_state |= pin
            defval_state &= ~pin
            intcon_state |= pin
        elif int_type == INT_LOW_LEVEL:
            inten_state |= pin
            defval_state |= pin
            intcon_state |= pin
        elif int_type == INT_CHANGE_LEVEL:
            inten_state |= pin
            intcon_state &= ~pin
        self.write_reg(GPINTEN + port, inten_state)
        self.write_reg(DEFVAL + port, defval_state)
        self.write_reg(INTCON + port, intcon_state)

    # Read the INTF register of the corresponding port
    def read_intf(self, port):
        return self.read_reg(INTF + port)

    # Read the INTCAP register of the corresponding port
    def read_intcap(self, port):
        return self.read_reg(INTCAP + port)

    # Read the GPIO register of the corresponding port
    def read_gpio(self, port):
        return self.read_reg(GPIO + port)

    # Read the OLAT register of the corresponding port
    def read_olat(self, port):
        return self.read_reg(OLAT + port)
        # Set the level of MCP23017 specified port

    def write_gpio(self, port, value):
        self.write_reg(GPIO + port, value)

    # Set the level of the specified pin of the specified port of MCP23017
    def set_gpio_pin(self, port, pin, value):
        gpio_state = self.read_reg(GPIO + port)
        if value == HIGH:
            gpio_state |= pin
        elif value == LOW:
            gpio_state &= ~pin
        self.write_reg(GPIO + port, gpio_state)


# Interrupt service function triggered by interrupt pin
def int_callback():
    print("portB:", hex(mcp23017.read_gpio(PORTB)))


if __name__ == '__main__':
    mcp23017 = MCP23017()
    mcp23017.set_port_dir(PORTA, OUTPUT)  # config PORTA as output
    mcp23017.set_port_dir(PORTB, OUTPUT)  # config PORTA as input
    mcp23017.set_io_pu(PORTB, PIN_ALL, ENABLE)  # PORTB enable pullup
    mcp23017.set_io_int(PORTB, PIN_ALL,
                        INT_CHANGE_LEVEL)  # Set the interrupt mode of all pins of PORTB port to level change
    # INT_EDGE_FALLING/INT_EDGE_RISING/INT_EDGE_BOTH/INT_EDGE_SETUP
    wpi.wiringPiISR(PIN_INTB, wpi.INT_EDGE_BOTH, int_callback)  # PIN INTB configuration

    print("portB INTCAP:", hex(mcp23017.read_intcap(PORTB)))
    print("portB:", hex(mcp23017.read_gpio(PORTB)))

    while True:
        print("port A ouput high")
        mcp23017.set_gpio_pin(PORTA, PIN0, HIGH)
        mcp23017.set_gpio_pin(PORTA, PIN1, HIGH)
        mcp23017.set_gpio_pin(PORTA, PIN2, HIGH)
        mcp23017.set_gpio_pin(PORTA, PIN3, HIGH)
        mcp23017.set_gpio_pin(PORTA, PIN4, HIGH)
        mcp23017.set_gpio_pin(PORTA, PIN5, HIGH)
        mcp23017.set_gpio_pin(PORTA, PIN6, HIGH)
        mcp23017.set_gpio_pin(PORTA, PIN7, HIGH)
        mcp23017.set_gpio_pin(PORTB, PIN0, HIGH)
        mcp23017.set_gpio_pin(PORTB, PIN1, HIGH)
        mcp23017.set_gpio_pin(PORTB, PIN2, HIGH)
        mcp23017.set_gpio_pin(PORTB, PIN3, HIGH)
        mcp23017.set_gpio_pin(PORTB, PIN4, HIGH)
        mcp23017.set_gpio_pin(PORTB, PIN5, HIGH)
        mcp23017.set_gpio_pin(PORTB, PIN6, HIGH)
        mcp23017.set_gpio_pin(PORTB, PIN7, HIGH)
#         mcp23017.write_gpio(PORTA, 0xFF)
#         mcp23017.write_gpio(PORTB, HIGH)
#         print("portA:",hex(mcp23017.read_gpio(PORTA)))
#         print("portB:",hex(mcp23017.read_gpio(PORTB)))
        time.sleep(1)
        print("port A ouput low")
        mcp23017.set_gpio_pin(PORTA, PIN0, LOW)
        mcp23017.set_gpio_pin(PORTA, PIN1, LOW)
        mcp23017.set_gpio_pin(PORTA, PIN2, LOW)
        mcp23017.set_gpio_pin(PORTA, PIN3, LOW)
        mcp23017.set_gpio_pin(PORTA, PIN4, LOW)
        mcp23017.set_gpio_pin(PORTA, PIN5, LOW)
        mcp23017.set_gpio_pin(PORTA, PIN6, LOW)
        mcp23017.set_gpio_pin(PORTA, PIN7, LOW)
        mcp23017.set_gpio_pin(PORTB, PIN0, LOW)
        mcp23017.set_gpio_pin(PORTB, PIN1, LOW)
        mcp23017.set_gpio_pin(PORTB, PIN2, LOW)
        mcp23017.set_gpio_pin(PORTB, PIN3, LOW)
        mcp23017.set_gpio_pin(PORTB, PIN4, LOW)
        mcp23017.set_gpio_pin(PORTB, PIN5, LOW)
        mcp23017.set_gpio_pin(PORTB, PIN6, LOW)
        mcp23017.set_gpio_pin(PORTB, PIN7, LOW)
#         mcp23017.write_gpio(PORTA, 0x00)
#         mcp23017.write_gpio(PORTB, LOW)
#         print("portA:",hex(mcp23017.read_gpio(PORTA)))
#         print("portB:",hex(mcp23017.read_gpio(PORTB)))
        time.sleep(1)
