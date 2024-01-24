import os

# checks the environment variable MOTION_COMPUTER_IP
# and defaults to localhost if it is not set
# this will allow us to copy over the code to the motion computer
# and run it without having to change the code
MOTION_COMPUTER_IP = os.getenv('MOTION_COMPUTER_IP', '127.0.0.1') 
MOTION_COMPUTER_PORT = 4001
NL2_IP = '127.0.0.1'
NL2_PORT = 15151
FRAME_RATE = 30 # transmission rate in hz
LOGGING = False #make true to generate logs