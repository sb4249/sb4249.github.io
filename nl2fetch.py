from packet import Packet
import math_utils
from nl2telemetry import NoLimits2
from nl2telemetry.message import get_telemetry, Answer
from nl2telemetry.message.reply import TelemetryData

class NL2Fetch:

    def __init__(self, ip, port):
        # Initialize NL2 connection here
        print("starting nl2 connection")
        self.nl2 = NoLimits2(ip, port)
        self.lastPos = None


    def NL2_get_telemetry(self, packet: Packet):
        self.nl2.send(get_telemetry)
        data = Answer.get_data(self.nl2.receive())

        if not isinstance(data, TelemetryData):
             # TODO: Handle error
             return
        
        if self.lastPos is None:
            self.lastPos = (data.x_pos, data.y_pos, data.z_pos)
        
        velocity = math_utils.calculate_velocity(self.lastPos, (data.position_x, data.position_y, data.position_z))
        packet.x_lin_vel = velocity[0]
        packet.y_lin_vel = velocity[1]
        packet.z_lin_vel = velocity[2]

        x, y, z, w = data.rotation_quaternion_x, data.rotation_quaternion_y, data.rotation_quaternion_z, data.rotation_quaternion_w
        pitch, roll = math_utils.quaternion_to_pitch_and_roll(x, y, z, w)
        packet.pitch_pos = pitch
        packet.roll_pos = roll

        self.lastPos = (data.position_x, data.position_y, data.position_z)

    def __del__(self):
        # Terminate NL2 connection here
        print("closing nl2 connection")
        self.nl2.close()
