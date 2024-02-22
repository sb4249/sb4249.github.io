"""This module performs the conversions needed to convert NoLimits2 data into a form usable by the motion computer."""

from scipy.spatial.transform import Rotation

last_pitch = 0
safety_counter = 0
safety_mode = False

def quaternion_to_pitch_and_roll(x, y, z, w):
    """This function converts quaternions from NoLimits2 representing the rotation of the roller-coaster cart in 3D space (x, y, z, and w) into pitch and roll angles in degrees. It does this with an external library called scipy.
    
    :param x: Rotation quaternion x.  
    :param y: Rotation quaternion y.  
    :param z: Rotation quaternion z. 
    :param w: Rotation quaternion w.  
    
    :return: The pitch and roll angles of the roller-coaster cart.
    """

    global last_pitch, safety_counter, safety_mode
    quaternion = Rotation.from_quat([x, y, z, w])
    euler_angles = quaternion.as_euler('xzy', degrees=True)

    pitch, roll, _ = euler_angles
    
    if (pitch > 0 and pitch-last_pitch >= 0.5): # Will have to be changed with testing. "0.5" should be replaced with the large single-frame delta seen in the test where an interlock occurred.
        safety_counter += 1
    elif (pitch <= 0):
        safety_mode = False
        safety_counter = 0
    
    if (safety_counter >= 5): # Will also have to be changed in testing. Can modify the sensitivity of safety mode.
        safety_mode = True
        
    if (safety_mode and pitch > 29.4): # Final thing that may need tweaking. 29.4 is the maximum angle achievable by the hardware, but orchestrated motion may make this more complicated.
        pitch = pitch * 0.9

    last_pitch = pitch
    return pitch, roll

def calculate_velocity(lastPos, currentPos, timeDiff=0.03333333333):
    """This function calculates the linear velocity in the x, y, and z directions for a given frame. It does this by taking the differnece in x, y, and z positions between frames and divides that by the time ellapsed over the frame (or 1/FramesPerSecond).
    
    :param lastPos: A tuple containin the position of the roller-coaster cart last frame.  
    :param currentPos: A tuple containing the position of the roller-coaster cart this frame.  
    :param timeDiff: The amount of time in seconds ellapsed over each frame. Dependent on frame rate data is being sent at.  
    
    :return: The linear velocity of the cart in the x, y, and z directions.
    """
    pos1 = tuple(lastPos)
    pos2 = tuple(currentPos)

    vx = (pos2[0] - pos1[0]) / time_diff
    vy = (pos2[1] - pos1[1]) / time_diff
    vz = (pos2[2] - pos1[2]) / time_diff
    
    return vx, vy, vz
