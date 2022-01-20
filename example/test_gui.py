#!/usr/bin/env python3

"""
License: You are free to use any part of code in this project as long as you mention original authors of this program:
Alpha Team composed of: Nirmalraj JEYANATHAN Joseph - SERFATY Milan - YE Hang - ZHANG Yujia

Supervised by Aurore (aurore.isep@gmail.com) and Hugo (myrobotswillconquertheworld@gmail.com)
IE.3510 (System Modeling) - ISEP 2022
"""

import time

from robot import Robot

# Robot properties
ROBOT_LENGTH = 0
MOTOR_PORTS = {}
SENSOR_PORTS = {}

# Communication with GUI
GUI_ADDRESS = {"host": "172.20.10.3", "port": 5204}

if __name__ == '__main__':
    robot = Robot(ROBOT_LENGTH, MOTOR_PORTS, SENSOR_PORTS, GUI_ADDRESS)
    while True:
        time.sleep(1)
        robot.socket._msg_to_send[0] = 5
