"""This module facilitates communication between the show computer and the motion computer."""

import socket

class Client:
    """This class contains all of the neccesary functions to initiate communication with the motion computer, send data to the motion computer, and close the socket conenction to the motion computer."""
    def __init__(self, ip, port):
        """Initializes objects needed for network connection."""
        self.ip = ip
        """The IP of the motion computer."""
        self.port = port
        """The port that the motion computer will communicate on."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        """The socket object used for communication between the show computer and the motion computer."""

    def send_data(self, data):
        """This function sends a formatted packet of motion data for one frame to the motion computer."""
        try:
            self.client_socket.sendto(data, (self.ip, self.port))

        except Exception as e:
            print("Error: ", e)

    def __del__(self):
        self.client_socket.close()
