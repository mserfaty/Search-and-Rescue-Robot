#!/usr/bin/env python3

"""
License: You are free to use any part of code in this project as long as you mention original authors of this program:
Alpha Team composed of: Nirmalraj JEYANATHAN Joseph - SERFATY Milan - YE Hang - ZHANG Yujia

Supervised by Aurore (aurore.isep@gmail.com) and Hugo (myrobotswillconquertheworld@gmail.com)
IE.3510 (System Modeling) - ISEP 2022
"""

import time

from ev3dev2.sensor import INPUT_3
from ev3dev2.motor import OUTPUT_A, OUTPUT_D

from robot import Robot

ROBOT_LENGTH = 110.2  # Value to adjust

MOTOR_PORTS = {"wheel_right": OUTPUT_A, "wheel_left": OUTPUT_D}
SENSOR_PORTS = {"gyro_sensor": INPUT_3}

if __name__ == '__main__':
    robot = Robot(ROBOT_LENGTH, MOTOR_PORTS, SENSOR_PORTS)

    # robot.move.go_to_coords(150, 200, 200, wait_until_not_moving=True)
    robot.move.turn_right(200, 1*360, use_gyro=False)
    time.sleep(1)
