"""This module facilitates communication between the show computer and the motion computer."""

import socket
import struct

class Client:
    """This class contains all of the neccesary functions to initiate
    communication with the motion computer, send and receive data with the motion computer, and close the socket conenction to the motion computer."""
    def __init__(self, ip: str, port: int):
        """Initializes objects needed for network connection."""
        self.ip = ip
        """The IP of the motion computer."""
        self.port = port
        """The port that the motion computer will communicate on."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        """The client socket for sending and receiving"""
        # Bind the socket
        self.client_socket.bind((ip, 4001)) #4002 when testing locally
        # Set timeout so that the listening thread can react to a program termination"""
        self.client_socket.settimeout(1) #one second (could maybe be less, but I don't see this becoming an issue)

    def send_data(self, data) -> None:
        """This function sends a formatted packet of motion data for one frame to the motion computer.

        :param data: Data set to be sent to the motion computer. Should be a correctly formatted packet for this application.

        :return: None
        """
        try:
            self.client_socket.sendto(data, (self.ip, self.port))

        except Exception as e:
            print("Error: ", e)

    def rec_data(self):
        """This function receives a command message packet from the motion computer"""

        try:
            data, address = self.client_socket.recvfrom(1024)
            command_msg = struct.unpack('lBBBB', data)

            # Temporary logic to interpret command type for testing
            commands = ["NO_COMMAND", "START_LOAD_LANGUAGE_1_COMMAND",
            "DOOR_OPENED_COMMAND", "DOOR_CLOSED_COMMAND",
            "GAME_START_COMMAND", "STOP_END_OF_GAME_COMMAND",
            "STOP_AUTO_COMMAND", "STOP_MANUAL_COMMAND",
            "START_LOAD_LANGUAGE_2_COMMAND",
            "START_LOAD_LANGUAGE_3_COMMAND", "START_LOAD_DEMO_COMMAND",
            "NUMBER_OF_GAME_COMMAND"]
            print("Command message recieved:", commands[command_msg[1]])

        except socket.timeout:
            #When the timer runs out, exit the function"""
            return
        except Exception as e:
            print("error recieving: ", e)

    def __del__(self):
        """Close the socket when the object goes out of scope"""
        self.client_socket.close()

