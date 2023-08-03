import sacn
import time
import sys

if len(sys.argv) < 2:
    print("Please provide an index value between 0 and 39 as an argument.")
    sys.exit(1)

index = int(sys.argv[1])

if index < 0 or index >= 40:
    print("Index value should be between 0 and 39.")
    sys.exit(1)

sender = sacn.sACNsender(fps=60)
sender.start()
sender.activate_output(1)
sender[1].multicast = False
sender[1].destination = "10.10.7.17"

# Create the tuple with 255 value at the specified index
dmx_tuple = tuple(255 if i == index else 0 for i in range(40))
sender[1].dmx_data = dmx_tuple
print(f"Sent DMX Values - index {index} on")

time.sleep(1) # You can adjust this sleep time as needed

sender.stop()
