#!/usr/bin/env python3
import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_D

from robot import Robot

# Robot properties
MOTOR_PORTS = {"wheel_right": OUTPUT_A, "wheel_left": OUTPUT_D}
ROBOT_LENGTH = 150.5  # 141
ROBOT_LENGTH_SPIRAL = 150.2

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


def parallel_pattern_def():
    """Generate coordinates for parallel pattern with specified width between patterns"""

    # Create list of coordinates (Tuple) between 0 and 1000 mm
    if PARALLEL_PATTERN_FRONT:
        pattern = [(x, y) for x in range(0, 1001, PATTERN_WIDTH) for y in (0, 1000)]
    elif PARALLEL_PATTERN_SIDE:
        pattern = [(y, x) for x in range(0, 1001, PATTERN_WIDTH) for y in (0, 1000)]
    else:
        raise ValueError("No pattern specified")

    # Reorder list to have the parallel pattern
    try:
        for i in range(0, len(pattern), 4):
            pattern[i + 2], pattern[i + 3] = pattern[i + 3], pattern[i + 2]
    except IndexError:
        pass

    # Put Origin to last element of list
    pattern.append(pattern[0])
    if PARALLEL_PATTERN_SIDE:
        pattern[0] = (0, 50)
    else:
        pattern.pop(0)
    return pattern


def spiral_pattern_def():
    """Generate coordinates for spiral pattern with specified width between patterns"""
    area_max_value = 1000 - 200
    # Create list of coordinates (Tuple) between 0 and 1000 mm
    list1 = [(0, 0)]
    for x in range(PATTERN_WIDTH, int(area_max_value/2) + 1, PATTERN_WIDTH):
        list1.append((x, list1[-1][0]))

    list2 = [(x, area_max_value - x) for x in range(0, int(area_max_value/2) + 1, PATTERN_WIDTH)]
    list3 = [(x, x) for x in range(area_max_value, int(area_max_value/2) - 1, -PATTERN_WIDTH)]
    list4 = [(area_max_value - x, x) for x in range(0, int(area_max_value/2) + 1, PATTERN_WIDTH)]

    pattern = []
    for k in range(len(list1)):
        pattern.append(list1[k])
        pattern.append(list2[k])
        pattern.append(list3[k])
        pattern.append(list4[k])

    # Put Origin to last element of list
    pattern.append(pattern[0])
    pattern.pop(0)
    return pattern


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

    if PARALLEL_PATTERN_FRONT or PARALLEL_PATTERN_SIDE:
        robot = Robot(ROBOT_LENGTH, MOTOR_PORTS)
        execute_pattern(parallel_pattern_def())

    if SPIRAL_PATTERN:
        robot = Robot(ROBOT_LENGTH_SPIRAL, MOTOR_PORTS)
        execute_pattern(spiral_pattern_def())
