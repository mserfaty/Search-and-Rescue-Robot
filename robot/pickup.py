"""
License: You are free to use any part of code in this project as long as you mention original authors of this program:
Alpha Team composed of: Nirmalraj JEYANATHAN Joseph - SERFATY Milan - YE Hang - ZHANG Yujia

Supervised by Aurore (aurore.isep@gmail.com) and Hugo (myrobotswillconquertheworld@gmail.com)
IE.3510 (System Modeling) - ISEP 2022
"""

import time

from ev3dev2.motor import MediumMotor

TIMEOUT_ARM = 30
SPEED_ARMS = 500


class Pickup(object):
    def __init__(self, motor_port):
        self.motor = MediumMotor(motor_port)
        time.sleep(0.1)
        self.initialize_arms()

    def initialize_arms(self):
        self.move_arm(self.motor, SPEED_ARMS, 3500)
        time.sleep(4)
        self.motor.reset()
        time.sleep(0.1)
        self.open_for_detection()

    @staticmethod
    def move_arm(motor, speed, degrees):
        motor.speed_sp = speed
        time.sleep(0.1)
        motor.position_sp = degrees
        time.sleep(0.1)
        motor.run_to_abs_pos()

    def open_arms(self):
        self.move_arm(self.motor, SPEED_ARMS, -1500)
        self.motor.wait_until_not_moving(TIMEOUT_ARM)
        time.sleep(4)

    def close_arms(self):
        self.move_arm(self.motor, SPEED_ARMS, -3800)
        self.motor.wait_until_not_moving(TIMEOUT_ARM)
        time.sleep(4)

    def open_for_detection(self):
        self.move_arm(self.motor, SPEED_ARMS, -1500)
        self.motor.wait_until_not_moving(TIMEOUT_ARM)
        time.sleep(4)
