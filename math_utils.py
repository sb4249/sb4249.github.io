from scipy.spatial.transform import Rotation

last_pitch = 0
safety_counter = 0
safety_mode = False

def quaternion_to_pitch_and_roll(x, y, z, w):
    global last_pitch, safety_counter, safety_mode

    quaternion = Rotation.from_quat([x, y, z, w])
    euler_angles = quaternion.as_euler('xzy', degrees=True)

    pitch, roll, _ = euler_angles
    
    if (pitch > 0 and pitch-last_pitch >= 0.5): #Will have to be changed with testing. "0.5" should be replaced with the large single-frame delta seen in the test where an interlock occurred.
        safety_counter += 1
    elif (pitch <= 0):
        safety_mode = False
        safety_counter = 0
    
    if (safety_counter >= 5): #Will also have to be changed in testing. Can modify the sensitivity of safety mode.
        safety_mode = True
        
    if (safety_mode):
        if (pitch > 29.4): #Final thing that may need tweaking. 29.4 is the maximum angle achievable by the hardware, but orchestrated motion may make this more complicated.
            pitch = pitch * 0.9

    last_pitch = pitch
    return pitch, roll

def calculate_velocity(last_pos, current_pos, time_diff=0.03333333333):
    pos1 = tuple(last_pos)
    pos2 = tuple(current_pos)

    vx = (pos2[0] - pos1[0]) / time_diff
    vy = (pos2[1] - pos1[1]) / time_diff
    vz = (pos2[2] - pos1[2]) / time_diff

    return vx, vy, vz

if __name__ == "__main__":
    x, y, z, w = 0.0075961, 0.0868241, 0.0868241, 0.9924039
    pitch, roll = quaternion_to_pitch_and_roll(x, y, z, w)
    print(f"Pitch: {pitch} degrees, Roll: {roll} degrees")

    last_pos = (10, 5, -3)
    current_pos = (10.6, 5.4, -4)

    velocity = calculate_velocity(last_pos, current_pos)
    print(f"Velocity: {velocity}")