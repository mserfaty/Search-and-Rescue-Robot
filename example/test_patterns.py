#!/usr/bin/env python3

"""
License: You are free to use any part of code in this project as long as you mention original authors of this program:
Alpha Team composed of: Nirmalraj JEYANATHAN Joseph - SERFATY Milan - YE Hang - ZHANG Yujia

Supervised by Aurore (aurore.isep@gmail.com) and Hugo (myrobotswillconquertheworld@gmail.com)
IE.3510 (System Modeling) - ISEP 2022
"""

import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_D

from robot import Robot
from robot.patterns import ParallelTrack, SpiralPattern

# Robot properties
MOTOR_PORTS = {"wheel_right": OUTPUT_A, "wheel_left": OUTPUT_D}
ROBOT_LENGTH = 135
ROBOT_LENGTH_SIDE = 125.5
ROBOT_LENGTH_SPIRAL = 135

# Speeds
AREA_SPEED = 200

# Tracks properties
PATTERN_WIDTH = 200  # Width of the patterns for parallel pattern detection
PARALLEL_PATTERN_FRONT = False
PARALLEL_PATTERN_SIDE = False
SPIRAL_PATTERN = True


def execute_pattern(pattern):
    """Execute specified pattern and detect objects during execution"""
    robot.move.mdiff.odometry_start()  # Start odometry to pattern coordinates of the robot

    # Go to each pair of coordinates in the list while detecting potential objects
    for coords in pattern:
        # print(coords)
        robot.move.go_to_coords(AREA_SPEED, coords[0], coords[1], wait_until_not_moving=True)

    robot.move.mdiff.odometry_stop()  # When pattern is finished, stop tracking coordinates
    print("FINISHED")
    time.sleep(100)


if __name__ == '__main__':
    # parallel_pattern = [(0, 1100), (200, 1100), (200, 200), (400, 200),
    #                   (400, 1100), (600, 1100), (600, 200), (800, 200),
    #                   (800, 1100), (0, 0)]

    # spiral_pattern = [(0, 1000), (1000, 1000), (1000, 0),
    #                   (100, 0), (100, 900), (900, 900), (900, 100),
    #                   (200, 100), (200, 800), (800, 800), (800, 200),
    #                   (300, 200), (300, 700), (700, 700), (700, 300),
    #                   (400, 300), (400, 600), (600, 600), (600, 400),
    #                   (500, 400), (500, 700), (500, 500), (500, 500)]

    if PARALLEL_PATTERN_FRONT:
        execute_pattern(ParallelTrack(parallel_pattern_front=True, track_width=PATTERN_WIDTH).pattern)
        robot = Robot(ROBOT_LENGTH, MOTOR_PORTS)
    elif PARALLEL_PATTERN_SIDE:
        execute_pattern(ParallelTrack(parallel_pattern_side=True, track_width=PATTERN_WIDTH).pattern)
        robot = Robot(ROBOT_LENGTH, MOTOR_PORTS)
    elif SPIRAL_PATTERN:
        robot = Robot(ROBOT_LENGTH_SPIRAL, MOTOR_PORTS)
        execute_pattern(SpiralPattern(PATTERN_WIDTH).pattern)