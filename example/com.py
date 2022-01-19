#!/usr/bin/env python3

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
