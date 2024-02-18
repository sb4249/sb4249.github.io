"""This module performs the conversions needed to convert NoLimits2 data into a form usable by the motion computer."""

from scipy.spatial.transform import Rotation

def quaternion_to_pitch_and_roll(x, y, z, w):
    """This function converts quaternions from NoLimits2 representing the rotation of the roller-coaster cart in 3D space (x, y, z, and w) into pitch and roll angles in degrees. It does this with an external library called scipy."""
    quaternion = Rotation.from_quat([x, y, z, w])
    eulerAngles = quaternion.as_euler('xzy', degrees=True)

    pitch, roll, _ = eulerAngles

    # pitch = max(-15.5, min(pitch, 33.75))
    # roll = max(-40, min(roll, 40))

    return pitch, roll

def calculate_velocity(lastPos, currentPos, timeDiff=0.03333333333):
    """This function calculates the linear velocity in the x, y, and z directions for a given frame. It does this by taking the differnece in x, y, and z positions between frames and divides that by the time ellapsed over the frame (or 1/FramesPerSecond)."""
    pos1 = tuple(lastPos)
    pos2 = tuple(currentPos)

    vx = (pos2[0] - pos1[0]) / timeDiff
    vy = (pos2[1] - pos1[1]) / timeDiff
    vz = (pos2[2] - pos1[2]) / timeDiff

    return vx, vy, vz