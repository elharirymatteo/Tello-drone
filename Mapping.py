import cv2
import numpy as np
from djitellopy import tello
import KeyPressModule as kp
from time import sleep
import math

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
angular_speed = 360/10  # Angular Speed (deg/s) (50deg/s) the drone takes 10s to turn 360 deg
interval = 0.25

dist_interval = forward_speed * interval
angular_interval = angular_speed * interval
#######################################################
x, y = 500, 500  # coordinates of our drone to be plotted
a, yaw = 0, 0  # initialize the angle and the yaw to zero
points = [(0, 0), (0, 0)]

kp.init()
agent = tello.Tello()
agent.connect()
print(agent.get_battery())


def get_keyboard_input():
    """
    lr: left, right
    fb: forward, backward
    ud: up, down
    yv: yaw velocity
    :return: 
    """""

    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 15
    global x, y, yaw, a
    d = 0

    if kp.get_key("LEFT"):
        lr = -speed
        d = dist_interval
        a = -180

    elif kp.get_key("RIGHT"):
        lr = speed
        d = -dist_interval
        a = 180

    if kp.get_key("UP"):
        fb = speed
        d = dist_interval
        a = 270

    elif kp.get_key("DOWN"):
        fb = -speed
        d = dist_interval
        a = -90

    if kp.get_key("a"):
        yv = -speed
        yaw -= angular_interval

    elif kp.get_key("d"):
        yv = speed
        yaw += angular_interval

    if kp.get_key("w"): ud = speed
    elif kp.get_key("s"): ud = -speed

    if kp.get_key("q"): agent.land()
    if kp.get_key("e"): agent.takeoff()

    sleep(0.2)  # add some delay to allow the computations to be accurate
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, a, d]


def draw_points(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)  # OpenCV uses BGR colours
    cv2.circle(img, points[-1], 8, (255, 0, 0), cv2.FILLED)  # OpenCV uses BGR colours
    cv2.putText(img, f'({(points[-1][0] - 500)/100}, {(points[-1][1] - 500)/100})m',
                    (points[-1][0] + 10, points[-1][1] + 30),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 100), 1)


while True:
    vals = get_keyboard_input()
    agent.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), np.uint8)
    points.append((vals[4], vals[5]))
    draw_points(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
