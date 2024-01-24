import os
import datetime
from nl2telemetry.message.reply import TelemetryData
from packet import Packet


def write(data: str, fileName: str):

    #get file path
    fileName += str(datetime.datetime.now())
    file = os.path.join("data", fileName)

    #writes it to the proper file, appending if already exists
    with open(file, "a") as output:
        output.write(data)


def log_nl2(nl2_data: TelemetryData):
    data = ""
    data += "position x: " + str(nl2_data.position_x) + "\n"
    data += "position y: " + str(nl2_data.position_y) + "\n"
    data += "position z: " + str(nl2_data.position_z) + "\n"
    
    data += "rotation_quaternion_x: " + str(nl2_data.rotation_quaternion_x) + "\n"
    data += "rotation_quaternion_y: " + str(nl2_data.rotation_quaternion_y) + "\n"
    data += "rotation_quaternion_z: " + str(nl2_data.rotation_quaternion_z) + "\n"
    data += "rotation_quaternion_w: " + str(nl2_data.rotation_quaternion_w) + "\n"

    write(data=data, fileName="nl2_data")

def log_packet(packetData: Packet):
    data = ""
    data += "x_lin_vel: " + str(packetData.x_lin_vel) + "\n"
    data += "y_lin_vel: " + str(packetData.y_lin_vel) + "\n"
    data += "z_lin_vel: " + str(packetData.z_lin_vel) + "\n"

    data += "pitch_pos: " + str(packetData.pitch_pos) + "\n"
    data += "roll_pos: " + str(packetData.roll_pos) + "\n"

    write(data=data, fileName="packet_data")
