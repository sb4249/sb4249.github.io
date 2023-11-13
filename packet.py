
import mathTest
import csv

class Packet:

    def __init__(self, x_lin_vel, y_lin_vel, z_lin_vel, pitch_ang_vel, roll_ang_vel, pitch_pos, roll_pos, altitude):
        self.x_lin_vel = x_lin_vel
        self.y_lin_vel = y_lin_vel
        self.z_lin_vel = z_lin_vel
        self.pitch_ang_vel = pitch_ang_vel
        self.roll_ang_vel = roll_ang_vel
        self.pitch_pos = pitch_pos
        self.roll_pos = roll_pos
        self.altitude = altitude
        self.tick = 0
        self.temp = 0

    def nl2_to_dict(file_name):

        with open(file_name) as f:
            data = csv.DictReader(f)
            dict_list = list(data)
        
        return dict_list
            
    def format_packet(dict_list):
        packets = []
        for dict in dict_list:
            x = dict["rotation_quaternion_x"]
            y = dict["rotation_quaternion_y"]
            z = dict["rotation_quaternion_z"]
            w = dict["rotation_quaternion_w"]

            pitch, roll = mathTest.quaternion_to_pitch_and_roll(x, y, z, w)

            pos_x = dict["position_x"]
            pos_y = dict["position_y"]
            pos_z = dict["position_z"]

            x_vel, y_vel, z_vel = mathTest.calculate_velocity((pos_x,pos_y,pos_z))

            packet = Packet(x_vel, y_vel, z_vel, pitch, roll)
            packets.append(packet)

        return packets



    def time_tick(self):
        self.tick += 1
