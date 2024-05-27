"""This module acts as a wrapper for all of the other modules. It initializes the client socket and NoLimits2 connection and loops through recieving data, constructing a packet, and sending it to the motion computer."""

import signal
import sys
import time
import threading
from packet import Packet
from client import Client
from nl2fetch import NL2Fetch
from globals import *

lock = threading.Lock() #lock for the kill_signal variable

""" Listening thread of execution """
def listener():
    global kill_signal
    while True:
        # If main thread received the kill signal, terminate this thread too
        with lock:
            if kill_signal:
                return

        # Receive data (should not be framerate synced)
        client.rec_data()

if __name__ == "__main__":

    global kill_signal
    kill_signal = False

    # Initialize client socket
    client = Client(MOTION_COMPUTER_IP, MOTION_COMPUTER_PORT)

    # Initialize NL2 connection (try 10 times before timing out)
    print("Connecting to NL2...")
    counter = 0
    nl2 = None
    while True:
        try:
            nl2 = NL2Fetch(NL2_IP, NL2_PORT)
            break
        except ConnectionRefusedError as e:
            counter += 1
            if counter >= 10:
                print("Failed to connect to NL2")
                exit(1)
            time.sleep(1.0)

    print("NL2 Connection Established")

    # Start listening thread of execution for message commands from MC
    listener_thread = threading.Thread(target=listener)
    listener_thread.start()

    # Handle graceful termination
    def signal_handler(sig, frame):
        global kill_signal
        # pass kill signal along to listening thread and wait for termination
        with lock:
            print("Exiting")
            kill_signal = True
        listener_thread.join()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # main data sending loop
    packet = Packet()
    while True:
        nl2.nl2_get_telemetry(packet)
        client.send_data(packet.format_packet())
        packet.time_tick()

        time.sleep(1.0/float(FRAME_RATE))

