import cv2
import numpy as np
import math
import serial

# Sends data to arduino via serial
# Data must be sent/received as S123456
# 123 = x servo angle, 456 = y servo angle
def send_data(arduino, x, y):
    message = 'S' + str(x).zfill(3) + str(y).zfill(3)
    arduino.write(message.encode())
    print(message)

# Connects serial port to arduino
def connect_arduino(port):
    port = '/dev/cu.usbmodem1442201'
    try:
        arduino = serial.Serial(port, 115200)
        return arduino
    except (FileNotFoundError, serial.serialutil.SerialException):
        print("No port at " + port)
        return False

# Calibrates cammera position
def calibrate_camera(img):
    worked = True
    img_blur = cv2.GaussianBlur(img,(3,3), sigmaX=0, sigmaY=0)
    hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
    # Find Red mask
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([8, 255, 255])
    mask_red  = cv2.inRange(hsv,lower_red,upper_red)
    # Find Blue mask
    lower_blue = np.array([105, 100, 100])
    upper_blue = np.array([135, 255, 255])
    mask_blue  = cv2.inRange(hsv,lower_blue,upper_blue)
    # Both Masks
    mask_all = mask_red + mask_blue

    mass_red_y, mass_red_x = np.where(mask_red >= 255)
    if (not mass_red_x.any()) or (not mass_red_y.any()):
        worked = False # If no blue is found
        return worked, 0, 0, 0, 0
    red_x = np.average(mass_red_x)
    red_y = np.average(mass_red_y)

    mass_blue_y, mass_blue_x = np.where(mask_blue >= 255)
    if (not mass_blue_x.any()) or (not mass_blue_y.any()):
        worked = False # If no blue is found
        return worked, 0, 0, 0, 0
    blue_x = np.average(mass_blue_x)
    blue_y = np.average(mass_blue_y)

    # Calculate scale (mm/pixles)
    scale_pixle = abs(red_y - blue_y)

    # Draw
    result = cv2.bitwise_and(img_blur, img_blur, mask=mask_all)
    result = cv2.circle(result, (int(red_x), int(red_y)), 5, (255, 0, 0), 2)
    result = cv2.circle(result, (int(blue_x), int(blue_y)), 5, (255, 0, 0), 2)

    return worked, red_x, red_y, scale_pixle, result

# # Connect to arduino via serial
# port = '/dev/cu.usbmodem1442201'
# arduino = connect_arduino(port)
# # Set to no tilt
# send_data(arduino, 90, 90)

# # Settup camera
# cam = cv2.VideoCapture(0)

# while True:
#     ret, img = cam.read()
#     img = cv2.flip(img[0:690, 300:929], -1)
#     worked, center_x, center_y, scale, result = calibrate_camera(img)
#     if worked:
#         print(scale)
#         cv2.imshow('mask', result)
#         cv2.waitKey(1)
#         break

# print('Center and Scale found')

# Finds raw x,y pixle ball position
def findBall(img):
    found = True
    x = 0
    y = 0

    img_blur = cv2.GaussianBlur(img,(3,3), sigmaX=0, sigmaY=0)
    hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([75, 255, 255])

    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    result = cv2.bitwise_and(img_blur, img_blur, mask=mask_yellow)

    mass_yellow_y, mass_yellow_x = np.where(mask_yellow >= 255)
    if (not mass_yellow_x.any()) or (not mass_yellow_y.any()):
        found = False # If no blue is found
        return found, 0, 0, 0
    yellow_x = np.average(mass_yellow_x)
    yellow_y = np.average(mass_yellow_y)

    result = cv2.circle(img, [int(yellow_x), int(yellow_y)], radius= 5, color = (255, 0, 0), thickness = 5)

    return found, yellow_x, yellow_y, result

# while True:
#     ret, img = cam.read()
#     img = cv2.flip(img[0:690, 300:929], -1)
#     found, x_pixle, y_pixle, result = findBall(img)
#     if found:
#         print(x_pixle)
#     cv2.imshow('FindBall', result)
#     cv2.waitKey(1)