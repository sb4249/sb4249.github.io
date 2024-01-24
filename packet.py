import struct
import csv

class Packet:

    # Default values are neutral machine position
    def __init__(self, x_lin_vel=0.0, y_lin_vel=0.0, z_lin_vel=0.0, pitch_pos=0.0, roll_pos=0.0):
        self.header = bytearray([0x00, 0x02, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.fsTimer = bytearray([0x00, 0x00, 0x00, 0xC0, 0x47, 0x61, 0x24, 0x40])
        self.tick = 0
        self.temp = 0 #unused
        self.x_lin_vel = x_lin_vel
        self.y_lin_vel = y_lin_vel
        self.z_lin_vel = z_lin_vel
        self.pitch_ang_vel = 0 #unused
        self.roll_ang_vel = 0 #unused
        self.pitch_pos = pitch_pos
        self.roll_pos = roll_pos
        self.altitude = 0 #unused
        self.garbage = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def format_packet(self):
        return struct.pack('8s8slidddddddd8s',
                            self.header,
                            self.fsTimer,
                            self.tick,
                            self.temp,
                            self.x_lin_vel,
                            self.y_lin_vel,
                            self.z_lin_vel,
                            self.pitch_ang_vel,
                            self.roll_ang_vel,
                            self.pitch_pos,
                            self.roll_pos,
                            self.altitude,
                            self.garbage)

    def time_tick(self):
        self.tick += 1

