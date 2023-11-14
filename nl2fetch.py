from packet import Packet
from mathTest import *

class NL2Fetch:

    def __init__(self, ip, port):
        # Initialize NL2 connection here
        print("starting nl2 connection")

    def __del__(self):
        # Terminate NL2 connection here
        print("closing nl2 connection")

    def NL2_get_telemetry(self, packet):
        # Fetch NL2 telemetry here to be used instead of the numbers

        velocity = calculate_velocity((10,5,-3),(10.6,5.4,-4))
        packet.x_lin_vel = velocity[0]
        packet.y_lin_vel = velocity[1]
        packet.z_lin_vel = velocity[2]

        x, y, z, w = 0.0075961, 0.0868241, 0.0868241, 0.9924039
        pitch, roll = quaternion_to_pitch_and_roll(x, y, z, w)
        packet.pitch_pos = pitch
        packet.roll_pos = roll

