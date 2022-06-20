from functions import *
import cv2
import time
import math

# Connect to arduino via serial
port = '/dev/cu.usbmodem1442201'
arduino = connect_arduino(port)
# Set to no tilt
send_data(arduino, 90, 90)

# Settup camera
cam = cv2.VideoCapture(0)

while True:
    x = input('X angle')
    if x == 'q':
        break
    send_data(arduino, x, 90)