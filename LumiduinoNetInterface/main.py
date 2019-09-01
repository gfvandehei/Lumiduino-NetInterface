
# ------------------------------------------------------------------------------
# Python program using the library to interface with the arduino sketch above.
# ------------------------------------------------------------------------------

import PyCmdMessenger
import time
from threading import Thread
from LumiduinoNetInterface.network import NetworkConnection
NetworkConnection()
'''
def recv_thread(c):
    while(True):
        print(c.receive())

# Initialize an ArduinoBoard instance.  This is where you specify baud rate and
# serial timeout.  If you are using a non ATmega328 board, you might also need
# to set the data sizes (bytes for integers, longs, floats, and doubles).  
arduino = PyCmdMessenger.ArduinoBoard("/dev/ttyACM0",baud_rate=115200)

# List of commands and their associated argument formats. These must be in the
# same order as in the sketch.
commands = [["s_info",""],
            ["s_cmds",""],
            ["s_ping",""],
            ["s_set_pixel","ssssss"],
            ["s_set_strip","sssss"],
            ["r_info","s"],
            ["r_cmds","s"],
            ["r_pong",""],
            ["r_ack",""],
            ["r_err","s"],
            ["r_unknown","s"],
            ["r_msg","s"]]

# Initialize the messenger
c = PyCmdMessenger.CmdMessenger(arduino,commands)
Thread(target=recv_thread, args=(c,)).start()
# Receive. Should give ["my_name_is",["Bob"],TIME_RECIEVED]
counter = 0
while True:
    c.send("s_set_pixel",0,counter,255,255,255,255)
    time.sleep(.01)
    counter += 1
    if counter == 120:
        counter = 0
        c.send("s_set_strip", 0, 0,0,0,255)'''


