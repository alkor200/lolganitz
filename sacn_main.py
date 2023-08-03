import sacn
import time
from loop_main import LightManager
from Light import StandardLight, MCPLight, Light
import mcp23017 as m

_gpio = [23, 22, 27, 17, 18, 15, 14, 4, 12, 25, 9, 1, 0, 11, 10, 24, 19, 13, 6, 5, 21, 20, 16, 26]
gpio = [23,
        22,
        27,
        17,
        18,
        15,
        14,
        12,
        25,
        9,
        10,
        (m.PORTA, m.PIN0),
        24,
        13,
        6,
        5,
        21,
        20,
        26,
        (m.PORTA, m.PIN7),
        (m.PORTA, m.PIN5),
        (m.PORTA, m.PIN3),
        (m.PORTA, m.PIN6),
        (m.PORTA, m.PIN1),
        (m.PORTA, m.PIN4),
        (m.PORTA, m.PIN2),
        (m.PORTB, m.PIN1),
        (m.PORTB, m.PIN2),
        (m.PORTB, m.PIN5),
        (m.PORTB, m.PIN4),
        (m.PORTB, m.PIN6),
        (m.PORTB, m.PIN7),
        (m.PORTB, m.PIN3),
        4,
        1,
        0,
        11,
        19,
        16,
        (m.PORTB, m.PIN0)]


light_list = []
i = 0
light_manager = LightManager(light_list)
for pin in gpio:
    if type(pin) is tuple:
        light_list.append(
            MCPLight(light_manager.mcp, pin[0], number=i, pin=pin[1])
        )
        i += 1
    else:
        light_list.append(
            StandardLight(number=i, pin=pin)
        )
        i += 1
# porta_portb = [m.PORTA, m.PORTB]
# for port in porta_portb:
    # for pin in m.PIN_TRANSLATE:

try:
    # start sACN receiver
    receiver = sacn.sACNreceiver()
    receiver.join_multicast(1)
    receiver.start()  # start the receiving thread

    @receiver.listen_on('universe', universe=1)  # listens on universe 1
    def callback(packet):  # packet type: sacn.DataPacket
        # print(packet.dmxData)  # print the received DMX data
        for count, dmx_value in enumerate(packet.dmxData[:40]):
            if dmx_value > 50:
                light_manager.lights[count].turn_on()
            else:
                light_manager.lights[count].turn_off()
    time.sleep(100)

except KeyboardInterrupt:
    receiver.stop()
    receiver.leave_multicast(1)
    light_manager.all_off()
    sys.exit(0)
except Exception as e:
    receiver.stop()
    receiver.leave_multicast(1)
    print(e)
    light_manager.all_off()
    pass
