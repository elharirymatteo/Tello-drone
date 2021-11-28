from djitellopy import tello
import KeyPressModule as kp
from time import sleep

kp.init()  # loads the pygame window with its keyboard listener
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
    speed = 50
    if kp.get_key("LEFT"): lr = -speed
    elif kp.get_key("RIGHT"): lr = speed

    if kp.get_key("UP"): fb = speed
    elif kp.get_key("DOWN"): fb = -speed

    if kp.get_key("a"): yv = speed
    elif kp.get_key("d"): yv = -speed

    if kp.get_key("w"): ud = speed
    elif kp.get_key("s"): ud = -speed

    if kp.get_key("q"): agent.land()
    if kp.get_key("e"): agent.takeoff()

    return [lr, fb, ud, yv]


while True:
    vals = get_keyboard_input()
    agent.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.1)
