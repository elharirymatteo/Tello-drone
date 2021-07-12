from djitellopy import tello
import cv2

agent = tello.Tello()
agent.connect()

print(agent.get_battery())

agent.streamon()

while True:
    img = agent.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)
