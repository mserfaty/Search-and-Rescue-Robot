#!/usr/bin/env python3

"""
License: You are free to use any part of code in this project as long as you mention original authors of this program:
Alpha Team composed of: Nirmalraj JEYANATHAN Joseph - SERFATY Milan - YE Hang - ZHANG Yujia

Supervised by Aurore (aurore.isep@gmail.com) and Hugo (myrobotswillconquertheworld@gmail.com)
IE.3510 (System Modeling) - ISEP 2022
"""

from ev3dev2.motor import OUTPUT_B

from robot import Robot

MOTOR_PORTS = {"pickup": OUTPUT_B}
ROBOT_LENGTH = 0

if __name__ == '__main__':
    robot = Robot(ROBOT_LENGTH, MOTOR_PORTS)

    robot.pickup.open_arms()
    robot.pickup.close_arms()
