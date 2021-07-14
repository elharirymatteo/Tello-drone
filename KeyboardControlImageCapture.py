from djitellopy import tello
import KeyPressModule as kp
import time
import cv2

kp.init()
agent = tello.Tello()
agent.connect()
print(agent.get_battery())

agent.streamon()


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

    if kp.get_key("q"):
        agent.land()
        time.sleep(3)
    if kp.get_key("e"): agent.takeoff()

    if kp.get_key("z"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(0.3)

    return [lr, fb, ud, yv]


while True:
    vals = get_keyboard_input()
    agent.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = agent.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)
