import cv2
import numpy as np
from djitellopy import tello
import KeyPressModule as kp

"""
This code is used to map the drone (odometry)
taking the distance and the angle we convert them in cartesian coordinates
to obtain the distance travelled and the new location of the drone

If we only rotate the drone, the only change will be in the heading and not in 
the coordinates, but if we both move forward and rotate the drone, to find the 
final coordinates we use basic goniometry 
"""
##################### PARAMETERS #######################
forward_speed = 117/10  # Forward Speed in cm/s (15cm/s) obtained empirically measuring distance covered after 10s
angular_speed = 360/10  # Angular Speed (deg/s) the drone takes 10s to turn 360 deg
interval = 0.25

dist_interval = forward_speed * interval
angular_interval = angular_speed * interval
#######################################################

kp.init()
agent = tello.Tello()
agent.connect()
print(agent.get_battery())


def get_keyboard_input():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    if kp.get_key("LEFT"): lr = -speed
    elif kp.get_key("RIGHT"): lr = speed

    if kp.get_key("UP"): fb = -speed
    elif kp.get_key("DOWN"): fb = speed

    if kp.get_key("a"): yv = -speed
    elif kp.get_key("d"): yv = speed

    if kp.get_key("w"): ud = -speed
    elif kp.get_key("s"): ud = speed

    if kp.get_key("q"): agent.land()
    if kp.get_key("e"): agent.takeoff()

    return [lr, fb, ud, yv]


def draw_points():
    cv2.circle(img, (300, 500), 20, (0, 0, 255), cv2.FILLED)


while True:
    vals = get_keyboard_input()
    agent.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), np.uint8)
    draw_points()
    cv2.imshow("Output", img)
    cv2.waitKey(1)
