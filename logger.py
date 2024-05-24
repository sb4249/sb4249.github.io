"""This module handles logging for the application. Will log information recieved from NoLimits2 and the packet that is constructed from it."""

import os
import datetime
from datetime import datetime
from nl2telemetry.message.reply import TelemetryData
from packet import Packet

frameNum = 0

def write(data: str, fileName: str) -> None:
    """This function is the on actually writing data to a log file. It will find the file and write the provided data to it if it is emtpy and append the data if it already contains some.
    
    :param data: Data that is to be written in a particular location. This will be the log data the program is trying to write.  
    :param fileName: The log file that data is being written to.  
    
    :return: None.
    """

    #get file path
    file = os.path.join("data", fileName)

    #writes it to the proper file, appending if already exists
    with open(file, "a") as output:
        output.write(data)


def log_nl2(nl2_data: TelemetryData) -> None:
    """This function retrieves data from NoLimits2, formats it into the correct form for a log file, and then writes it to a log file called `nl2_data`
    
    :param nl2_data: Unmodified motion data for a particular frame recieved from NoLimits2.  
    
    :return: None.
    """
    frameNum = frameNum + 1
    
    now = datetime.now()
    
    data = "Current Time: " + now + "\n"
    data += "Frame number: " + frameNum + "\n"
    data += "position x: " + str(nl2_data.position_x) + "\n"
    data += "position y: " + str(nl2_data.position_y) + "\n"
    data += "position z: " + str(nl2_data.position_z) + "\n"
    
    data += "rotation_quaternion_x: " + str(nl2_data.rotation_quaternion_x) + "\n"
    data += "rotation_quaternion_y: " + str(nl2_data.rotation_quaternion_y) + "\n"
    data += "rotation_quaternion_z: " + str(nl2_data.rotation_quaternion_z) + "\n"
    data += "rotation_quaternion_w: " + str(nl2_data.rotation_quaternion_w) + "\n"

    write(data=data, fileName="nl2_data")

def log_packet(packetData: Packet) -> None:
    """This function retrieves data from the packets the applcation constructs, formats it into the correct form for a log file, and then writes it to a log file called `packet_data`
    
    :param packetData: Motion data formatted into a packet that is readable by the motion computer and ready to be sent.  
    
    :return: None.
    """
        
    now = datetime.now()
    
    data = "Current Time: " + now + "\n"
    data += "Frame number: " + frameNum + "\n"
    data += "x_lin_vel: " + str(packetData.x_lin_vel) + "\n"
    data += "y_lin_vel: " + str(packetData.y_lin_vel) + "\n"
    data += "z_lin_vel: " + str(packetData.z_lin_vel) + "\n"

    data += "pitch_pos: " + str(packetData.pitch_pos) + "\n"
    data += "roll_pos: " + str(packetData.roll_pos) + "\n"

    write(data=data, fileName="packet_data")
