"""This module is responsible for constructing the motion data packet in a form usable by the motion computer."""

import struct
import csv

class Packet:
    """This class takes the values that the application has transformed as input (linear velocity in the x, y, and z direction, pitch angle, and roll angle) and constructs a packet from them that is readable by the motion computer. The whole packet should be exactly 88 bytes long."""

    # Default values are neutral machine position
    def __init__(self, x_lin_vel=0.0, y_lin_vel=0.0, z_lin_vel=0.0, pitch_pos=0.0, roll_pos=0.0):
        """This function initializes variables that will be necessary to construct a properly formatted packet."""
        self.header: bytearray = bytearray([0x00, 0x02, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00])
        """A header for the packets that will be sent. Mostly buffer bytes to allow packet to be correct size."""
        self.fsTimer: bytearray = bytearray([0x00, 0x00, 0x00, 0xC0, 0x47, 0x61, 0x24, 0x40])
        """Information necessary for the motion computer's timer."""
        self.tick: int = 0
        """The frame that is currently being processed"""
        self.temp: int = 0 #unused
        """An unused variable in the motion computer."""
        self.x_lin_vel: int = x_lin_vel
        """Linear velocity in the x direction for a particular frame."""
        self.y_lin_vel: int = y_lin_vel
        """Linear velocity in the y direction for a particular frame."""
        self.z_lin_vel: int = z_lin_vel
        """Linear velocity in the z direction for a particular frame."""
        self.pitch_ang_vel: int = 0 #unused
        """An unused variable in the motion computer."""
        self.roll_ang_vel: int = 0 #unused
        """An unused variable in the motion computer."""
        self.pitch_pos: int = pitch_pos
        """The pitch angle of the roller-coaster cart for a particular frame."""
        self.roll_pos: int = roll_pos
        """The roll angle of the roller-coaster cart for a particular frame."""
        self.altitude: int = 0 #unused
        """An unused variable in the motion computer."""
        self.garbage: bytearray = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        """Buffer data at the end of the packet to allow it to be the correct size to be accepted by the motion computer. Must be exactly 8 bytes."""

    def format_packet(self) -> struct.pack:
        """This function formats the packet that will be sent to the motion computer.
        
        :return: A correctly constructed packet that can be sent to the motion computer.
        """
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

    def time_tick(self) -> None:
        """This function incriments a variable that allows the application to track which frame is currently being processed.
        
        :return: None.
        """
        self.tick += 1

