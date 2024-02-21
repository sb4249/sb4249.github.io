from scipy.spatial.transform import Rotation

lastPitch = 0
safetyCounter = 0
safetyMode = False

def quaternion_to_pitch_and_roll(x, y, z, w):
    global lastPitch, safetyCounter, safetyMode

    quaternion = Rotation.from_quat([x, y, z, w])
    eulerAngles = quaternion.as_euler('xzy', degrees=True)

    pitch, roll, _ = eulerAngles
    
    if (pitch > 0 and pitch-lastPitch >= 0.5): #Will have to be changed with testing. "0.5" should be replaced with the large single-frame delta seen in the test where an interlock occurred.
        safetyCounter += 1
    elif (pitch <= 0):
        safetyMode = False
        safetyCounter = 0
    
    if (safetyCounter >= 5): #Will also have to be changed in testing. Can modify the sensitivity of safety mode.
        safetyMode = True
        
    if (safetyMode):
        if (pitch > 29.4): #Final thing that may need tweaking. 29.4 is the maximum angle achievable by the hardware, but orchestrated motion may make this more complicated.
            pitch = pitch * 0.9

    lastPitch = pitch
    return pitch, roll

def calculate_velocity(lastPos, currentPos, timeDiff=0.03333333333):
    pos1 = tuple(lastPos)
    pos2 = tuple(currentPos)

    vx = (pos2[0] - pos1[0]) / timeDiff
    vy = (pos2[1] - pos1[1]) / timeDiff
    vz = (pos2[2] - pos1[2]) / timeDiff

    return vx, vy, vz

if __name__ == "__main__":
    x, y, z, w = 0.0075961, 0.0868241, 0.0868241, 0.9924039
    pitch, roll = quaternion_to_pitch_and_roll(x, y, z, w)
    print(f"Pitch: {pitch} degrees, Roll: {roll} degrees")

    lastPos = (10, 5, -3)
    currentPos = (10.6, 5.4, -4)

    velocity = calculate_velocity(lastPos, currentPos)
    print(f"Velocity: {velocity}")