"""This module serves as communication with NoLimits2 and allows for the application to recieve motion data for each frame of the simulation."""

from packet import Packet
import math_utils
from nl2telemetry import NoLimits2
from nl2telemetry.message import get_telemetry, Answer
from nl2telemetry.message.reply import TelemetryData
from globals import FRAME_RATE, LOGGING
from logger import log_packet, log_nl2
import nl2telemetry.transmitter
from typing import Tuple

class NL2Fetch:
    """This class provides the functions necessary to connect to NoLimits2, recieve data, and close the connection when necessary."""

    def __init__(self, ip: str, port: int):
        """Initializes objects needed for network connection to NoLimits2."""
        # Initialize NL2 connection here
        print("starting nl2 connection")
        self.nl2: nl2telemetry.transmitter.TcpTransmitter = NoLimits2(ip, port)
        """Initializes an object that will allow the application to communicate with NoLimits2. This uses the nl2telemetry package to facilitate communication."""
        self.nl2.connect()
        self.last_pos: Tuple[int, int, int] = None
        """Initializes a variable to track the last position of the roller-coaster cart. This will be used to calculate linear velocity over each frame of the simulation. Each value in the tuple represents the x, y, and z position of the roller-coaster cart."""
        self.play_mode = False
        """Initializes a variable to track the if the game is still running. This is used to determine if the game was running but has exited."""


    def nl2_get_telemetry(self, packet: Packet) -> None:
        """This function recieves values from NoLimits2 including linear velocity in the x, y, and z directions and the rotation quaternions for the roller-coaster cart in 3D space. This data will later be manipulated to convert it into a form usable by the motion copmputer. The packet object is updated with the new values.
        
        :param packet: An instance of the packet class. Will be populated with data to send to the motion computer. 
        
        :return: None
        """
        self.nl2.send(get_telemetry)
        data = Answer.get_data(self.nl2.receive())

        if not isinstance(data, TelemetryData):
             print("Error getting telemetry data")
             return

        if data.in_play_mode:

            if (LOGGING):
                log_nl2(nl2_data=data)


            # if this is the first frame being received,
            # set the last position to the current position
            # for purposes of calculating velocity
            self.play_mode = True
            self.last_pos = self.last_pos or (data.position_x, data.position_y, data.position_z)

            velocity = math_utils.calculate_velocity(
                self.last_pos,
                (data.position_x, data.position_y, data.position_z),
                1.0/float(FRAME_RATE)
            )

            packet.x_lin_vel = velocity[0]
            packet.y_lin_vel = velocity[1]
            packet.z_lin_vel = velocity[2]

            x, y, z, w = data.rotation_quaternion_x, data.rotation_quaternion_y, data.rotation_quaternion_z, data.rotation_quaternion_w
            if (x, y, z, w) == (0, 0, 0, 0):
                print("Received zero quaternion, skipping")
                return
            pitch, roll = math_utils.quaternion_to_pitch_and_roll(x, y, z, w)
            packet.pitch_pos = pitch
            packet.roll_pos = roll

            self.last_pos = (data.position_x, data.position_y, data.position_z)

            if (LOGGING):
                log_packet(packetData=packet)

        elif self.play_mode == True:
            packet.x_lin_vel = 0.0
            packet.y_lin_vel = 0.0
            packet.z_lin_vel = 0.0
            packet.pitch_pos = 0.0
            packet.roll_pos = 0.0
            self.last_pos = None

    def __del__(self) -> None:
        """Closes the connection to NoLimits2 when the application is terminated."""
        print("closing nl2 connection")
        self.nl2.close()
