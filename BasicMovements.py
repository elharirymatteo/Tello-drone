from djitellopy import tello
from time import sleep

agent = tello.Tello()
agent.connect()

print(agent.get_battery())

agent.takeoff()
# agent.send_rc_control(0, 60, 0, 0)
sleep(2)
agent.send_rc_control(0, 0, 0, 90)
agent.land()
