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
    ret, img = cam.read()
    img = cv2.flip(img[0:690, 300:929], -1)
    worked, x_center, y_center, scale_pixle, result = calibrate_camera(img)
    if worked:
        print(scale_pixle)
        # cv2.startWindowThread()
        # cv2.imshow('mask', result)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.waitKey(1)
        break

print('Center and Scale found')

scale_mm = 135
scale = scale_mm / scale_pixle
x_setpoint = y_setpoint = 0

Kp_x = Kp_y = 0.5
Kd_x = Kd_y = 0.2

t_start = time.time()
t_last = t_start

x_last = x_setpoint
y_last = y_setpoint

while True:
    ret, img = cam.read()
    img = cv2.flip(img[0:690, 300:929], -1)
    found, x_pixle, y_pixle, result = findBall(img)
    if found:
        # Calculate x and y position from center in mm
        x = (x_pixle - x_center) * scale
        y = (y_center - y_pixle) * scale

        x_error = x - x_setpoint
        y_error = y - y_setpoint

        dT = time.time() - t_last
        t_last = time.time()

        x_der = (x_error - x_last) / dT
        y_der = (y_error - y_last) / dT

        x_last = x_error
        y_last = y_error

        x_angle = 90 + Kp_x * x_error + Kd_x * x_der
        y_angle = 90 + Kp_y * y_error + Kd_y * y_der

        if x_angle < 0: x_angle = 0
        else:
            if x_angle > 180: x_angle = 180
        if y_angle < 0: y_angle = 0
        else: 
            if y_angle > 180: y_angle = 180
        send_data(arduino, int(x_angle), int(y_angle))
        # print('X_angle: ' + str(x_angle) + ', Y_angle: ' + str(y_angle))