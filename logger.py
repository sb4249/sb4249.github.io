import json
import os


dataFromNL2 = {
    "speed": 0.0,
    "position_x": 0.0,
    "position_y": 0.0,
    "position_z": 0.0,
    "rotation_quaternion_x": 0.0,
    "rotation_quaternion_y": 0.0,
    "rotation_quaternion_z": 0.0,
    "g_force_x": 0.0,
    "g_force_y": 0.0,
    "g_force_z": 0.0
}

dataPostCalculations = {
    "speed": 0.0,
    "position_x": 0.0,
    "position_y": 0.0,
    "position_z": 0.0,
    "rotation_quaternion_x": 0.0,
    "rotation_quaternion_y": 0.0,
    "rotation_quaternion_z": 0.0,
    "g_force_x": 0.0,
    "g_force_y": 0.0,
    "g_force_z": 0.0
}

dataToBlackBox = {
    "state_flags": 0,
    "frame_number": 0,
    "view_mode": 0,
    "current_coaster": 0,
    "coaster_style_id": 0,
    "current_train": 0,
    "current_car": 0,
    "current_seat": 0,
    "speed": 0.0,
    "position_x": 0.0,
    "position_y": 0.0,
    "position_z": 0.0,
    "rotation_quaternion_x": 0.0,
    "rotation_quaternion_y": 0.0,
    "rotation_quaternion_z": 0.0,
    "g_force_x": 0.0,
    "g_force_y": 0.0,
    "g_force_z": 0.0
}

##takes in the data in the proper dictionary format as shown above
def write_json(dict_data, file: str):
    #serializes the object
    json_obj = json.dumps(dict_data, indent=4)

    #get file path
    file = os.path.join("data", file)
    #writes it to the proper file, appending if already exists
    with open(file, "a") as output:
        output.write(json_obj)


def log_nl2(nl2_data: []):
    dictionary_formatted_data = nl2_data #TODO(convert to dictionary)
    write_json(dictionary_formatted_data, "nl2_data.json")

def log_converted(conv_data: []):
    dictionary_formatted_data = nl2_data #TODO(convert to dictionary)
    write_json(dictionary_formatted_data, "converted_data.json")
    

def log_packet(packetData):
    dictionary_formatted_data = nl2_data #TODO(convert to dictionary)
    write_json(dictionary_formatted_data, "packet_data.json")
    


def sampleWrite():
    data = '{"speed":5.5, "position_y": 10.2}'
    write_json(json.loads(data), "sample_data.json")


if __name__=="__main__":
    #init all data files to empty
    open(os.path.join("data", "nl2_data.json"), 'w').close()
    open(os.path.join("data", "packet_data.json"), 'w').close()
    open(os.path.join("data", "converted_data.json"), 'w').close()
    open(os.path.join("data", "sample_data.json"), 'w').close()

    #call to see it tested:
    sampleWrite()