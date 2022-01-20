#!/usr/bin/env python3

import time

from ev3dev2.sensor import INPUT_4

from robot import Robot

# Robot properties
ROBOT_LENGTH = 0
MOTOR_PORTS = {}
SENSOR_PORTS = {"color_sensor": INPUT_4}

if __name__ == '__main__':
    robot = Robot(ROBOT_LENGTH, MOTOR_PORTS, SENSOR_PORTS)
    while True:
        detected_color = robot.color_sensor.rgb
        print(detected_color)
        time.sleep(1)

