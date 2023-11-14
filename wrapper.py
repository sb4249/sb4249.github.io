import signal
import sys
import time
from packet import Packet
from client import Client
from nl2fetch import NL2Fetch

if __name__ == "__main__":
    server_ip = '192.168.1.64'
    server_port = 4001
    rate = 30 # transmission rate in hz

    # Handle graceful termination
    def signal_handler(sig, frame):
        print("exiting")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Initialize client socket
    client = Client(server_ip, server_port)

    # Initialize NL2 connection
    nl2 = NL2Fetch(server_ip, server_port)

    packet = Packet()
    while True:

        nl2.NL2_get_telemetry(packet)
        client.send_data(packet.format_packet())
        packet.time_tick()

        time.sleep(1.0/float(rate))

