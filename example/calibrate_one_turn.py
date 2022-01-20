#!/usr/bin/env python3

"""
License: You are free to use any part of code in this project as long as you mention original authors of this program:
Alpha Team composed of: Nirmalraj JEYANATHAN Joseph - SERFATY Milan - YE Hang - ZHANG Yujia

Supervised by Aurore (aurore.isep@gmail.com) and Hugo (myrobotswillconquertheworld@gmail.com)
IE.3510 (System Modeling) - ISEP 2022
"""

from ev3dev2.sensor import INPUT_2
from ev3dev2.motor import OUTPUT_B, OUTPUT_C

from robot import Robot

# Robot properties
MOTOR_PORTS = {"wheel_left": OUTPUT_C, "wheel_right": OUTPUT_B}
SENSOR_PORTS = {"gyro_sensor": INPUT_2}

ROBOT_LENGTH = 133.5  # 133.9

# Speeds
AREA_SPEED = 170


def execute_track(track):
    """Execute specified track and detect objects during execution"""
    robot.move.mdiff.odometry_start()  # Start odometry to track coordinates of the robot

    # Go to each pair of coordinates in the list while detecting potential objects
    for coords in track:
        # print(coords)
        robot.move.go_to_coords(AREA_SPEED, coords[0], coords[1], wait_until_not_moving=True)

    robot.move.mdiff.odometry_stop()  # When track is finished, stop tracking coordinates
    print("FINISHED")
    # time.sleep(100)


if __name__ == '__main__':
    robot = Robot(ROBOT_LENGTH, MOTOR_PORTS, SENSOR_PORTS)

    turn = [(0, 1000), (1000, 1000), (1000, 0), (0, 0)]

    execute_track(turn)
