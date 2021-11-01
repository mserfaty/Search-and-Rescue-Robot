#!/usr/bin/env python3
import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, MoveDifferential
from ev3dev2.wheel import EV3EducationSetTire

from robot import Robot


ROBOT_LENGTH = 135.5
MOTOR_PORTS = {"left": OUTPUT_A, "right": OUTPUT_B}

#
# class Robot(object):
#     def __init__(self, motor_left_port=OUTPUT_A, motor_right_port=OUTPUT_B):
#         self.tank = MoveTank(motor_left_port, motor_right_port)
#         # self.motor_left = LargeMotor(motor_left_port)
#         # self.motor_right = LargeMotor(motor_right_port)
#         self.degrees = 360*5
#
#     def main(self):
#         """
#         Execute a Motor loop
#         """
#         # self.motor_left.on(100)
#         # self.motor_right.on(100)
#
#         # threading.Thread(target=self.motor_left.on_for_degrees, args=(50, self.degrees)).start()
#         # self.motor_right.on_for_degrees(50, self.degrees)
#         # time.sleep(1)
#         mdiff = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3EducationSetTire, 135.5)
#         mdiff.turn_right(25, 360)
#         # self.tank.on_for_degrees(25, -25, 241*4)
#
#         # self.tank.on_for_degrees(50, 50, 2045)
#         # time.sleep(2)
#         # self.tank.on_for_degrees(50, 0, 437)
#         # # self.tank.on_for_degrees(50, 0, 604)
#         # time.sleep(2)
#         # self.tank.on_for_degrees(50, 50, 2045)
#         # time.sleep(2)
#         # self.tank.on_for_degrees(50, 0, 437)
#         # time.sleep(2)
#         # self.tank.on_for_degrees(50, 50, 2045)
#         # time.sleep(2)
#         # self.tank.on_for_degrees(50, 0, 437)
#         # time.sleep(2)
#         # self.tank.on_for_degrees(50, 50, 2045)
#
#         # (0, 360*2.7) (90, 1062)
#         # thread = threading.Thread(target=self.motor_left.on_for_degrees, args=(50, 1062))
#         # thread.setDaemon(True)
#         # thread.start()
#         # self.motor_right.on_for_degrees(100, 0)
#
#         # time.sleep(1)
#         # threading.Thread(target=self.motor_left.on_for_degrees, args=(50, self.degrees)).start()
#         # self.motor_right.on_for_degrees(50, self.degrees)
#
#         time.sleep(3)
#
#         # print(self.motor_left.position)
#         # print(self.motor_right.position)
#         #
#         # self.motor_right.reset()
#         # self.motor_left.reset()


if __name__ == '__main__':
    robot = Robot(ROBOT_LENGTH, MOTOR_PORTS)
    # robot = Robot()  # Initialisation of the robot
    # robot.main()  # Execution of the Motor loop
    robot.move.go_straight(25, 100)


# from ev3dev2.sensor.lego import TouchSensor
# from ev3dev2.sensor.lego import UltrasonicSensor
# from ev3dev2.led import LED_GROUPS
# from ev3dev2.sound import Sound
#
# # ir = InfraredSensor()
# ts = TouchSensor()
# us = UltrasonicSensor()
# units = us.units
# sound = Sound()
#
# """Keep the IR sensor and US sensor in required modes"""
# # ir.mode = 'IR-PROX'
# us.mode = 'US-DIST-CM'  # Put the US sensor into distance mode. 74.4cm max
# while not ts.value():  # while loop runs as long as the touch sensor button is NOT pressed.When the touch sensor is pressed the loop is exited,
#     # a beep is sounded and the left LED is set to green
#     # distance = ir.value()
#     distance = us.value() / 10  # convert mm to cm
#     print(str(distance) + " " + units)
#
#     if distance < 60:
#         Leds.set_color(LED_GROUPS['LEFT'], Leds.RED)
#     else:
#         Leds.set_color(Leds.LEFT, Leds.GREEN)
#
# sound.beep()
# # Leds.set_color(Leds.LEFT, Leds.GREEN)
#
#
# # straight turn 30 90° left right
