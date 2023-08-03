import sacn
import time

sender = sacn.sACNsender(
    fps=180)  # provide an IP-Address to bind to if you want to send multicast packets from a specific interface
sender.start()  # start the sending thread
sender.activate_output(1)  # start sending out data in the 1st universe
sender[1].multicast = False  # set multicast to True
sender[1].destination = "10.10.7.17"
# Keep in mind that if multicast is on, unicast is not used

interval = 0.5
start_time = time.time()
high = True
while True:
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time >= interval:
        print(f"Action performed every {elapsed_time} seconds")
        if high:
            all_on_tuple = (255,) * 40
            sender[1].dmx_data = all_on_tuple
            print("Sent DMX Values - all on")
            high = False
        else:
            all_off_tuple = (0,) * 40
            sender[1].dmx_data = all_off_tuple
            print("Sent DMX Values - all off")
            high = True

        # Reset the start time for the next iteration
        start_time = time.time()

    time.sleep(0.01)

sender.stop()  # do not forget to stop the sender
