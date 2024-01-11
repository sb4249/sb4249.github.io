from packet import Packet
import math_utils
from nl2telemetry import NoLimits2
from nl2telemetry.message import get_telemetry, Answer
from nl2telemetry.message.reply import TelemetryData
from globals import FRAME_RATE

class NL2Fetch:

    def __init__(self, ip, port):
        # Initialize NL2 connection here
        print("starting nl2 connection")
        self.nl2 = NoLimits2(ip, port)
        self.nl2.connect()
        self.last_pos = None


    def nl2_get_telemetry(self, packet: Packet):
        self.nl2.send(get_telemetry)
        data = Answer.get_data(self.nl2.receive())

        if not isinstance(data, TelemetryData):
             # TODO: Handle error
             return
        
        # if this is the first frame being received,
        # set the last position to the current position
        # for purposes of calculating velocity
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
        pitch, roll = math_utils.quaternion_to_pitch_and_roll(x, y, z, w)
        packet.pitch_pos = pitch
        packet.roll_pos = roll

        self.last_pos = (data.position_x, data.position_y, data.position_z)

    def __del__(self):
        # Terminate NL2 connection here
        print("closing nl2 connection")
        self.nl2.close()
