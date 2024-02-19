"""This module contains important variables used repeatedly in the rest of the application."""

import os

# checks the environment variable MOTION_COMPUTER_IP
# and defaults to localhost if it is not set
# this will allow us to copy over the code to the motion computer
# and run it without having to change the code
MOTION_COMPUTER_IP = os.getenv('MOTION_COMPUTER_IP', '127.0.0.1')
"""The IP of the motion computer. This is where packets will be sent once they are formatted and generated."""
MOTION_COMPUTER_PORT = 4001
"""The port that communication with the motion computer is done on."""
NL2_IP = '127.0.0.1'
"""The IP that motion information is being recieved from. Should be localhost IP since NoLimits2 will be running on the show computer."""
NL2_PORT = 15151
"""The port that communcation with NoLimits2 is done on."""
FRAME_RATE = 30 # transmission rate in hz
"""The rate in Hz that the application sends motion data to the motion computer."""
LOGGING = False #make true to generate logs
"""A boolean dictating whether or not logs should be generated when the application is sending data."""