import signal
import sys
import time
from packet import Packet
from client import Client
from nl2fetch import NL2Fetch
from globals import *

if __name__ == "__main__":

    # Handle graceful termination
    def signal_handler(sig, frame):
        print("exiting")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Initialize client socket
    client = Client(MOTION_COMPUTER_IP, MOTION_COMPUTER_PORT)

    # Initialize NL2 connection
    nl2 = NL2Fetch(NL2_IP, NL2_PORT)

    packet = Packet()
    while True:

        nl2.NL2_get_telemetry(packet)
        client.send_data(packet.format_packet())
        packet.time_tick()

        time.sleep(1.0/float(FRAME_RATE))

