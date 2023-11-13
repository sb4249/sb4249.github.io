from scipy.spatial.transform import Rotation

def quaternion_to_pitch_and_roll(x, y, z, w):
    quaternion = Rotation.from_quat([x, y, z, w])
    eulerAngles = quaternion.as_euler('zyx', degrees=True)

    pitch, roll, _ = eulerAngles

    pitch = max(-15.5, min(pitch, 33.75))
    roll = max(-40, min(roll, 40))

    return pitch, roll

x, y, z, w = 0.0075961, 0.0868241, 0.0868241, 0.9924039

pitch, roll = quaternion_to_pitch_and_roll(x, y, z, w)
print(f"Pitch: {pitch} degrees, Roll: {roll} degrees")

def calculate_velocity(lastPos, currentPos, timeDiff=0.03333333333):
    pos1 = tuple(lastPos)
    pos2 = tuple(currentPos)

    vx = (pos2[0] - pos1[0]) / timeDiff
    vy = (pos2[1] - pos1[1]) / timeDiff
    vz = (pos2[2] - pos1[2]) / timeDiff

    return vx, vy, vz

lastPos = (10, 5, -3)
currentPos = (10.6, 5.4, -4)

velocity = calculate_velocity(lastPos, currentPos)
print(f"Velocity: {velocity}")