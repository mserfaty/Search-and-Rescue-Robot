"""
License: You are free to use any part of code in this project as long as you mention original authors of this program:
Alpha Team composed of: Nirmalraj JEYANATHAN Joseph - SERFATY Milan - YE Hang - ZHANG Yujia

Supervised by Aurore (aurore.isep@gmail.com) and Hugo (myrobotswillconquertheworld@gmail.com)
IE.3510 (System Modeling) - ISEP 2022
"""

import threading
import time

from ev3dev2.motor import SpeedNativeUnits, SpeedInvalid, MoveDifferential
from ev3dev2.wheel import EV3EducationSetTire


class SpeedTacho(SpeedNativeUnits):
    """
    Speed in tacho counts per second.
    """

    def to_percentage(self, motor=None):
        """
        Convert tacho speed to percentage
        """
        if self.native_counts > motor.max_speed:
            raise SpeedInvalid("invalid native-units: {} max speed {}, {} was requested".format(
                motor, motor.max_speed, self.native_counts))
        return self.native_counts * 100 / motor.max_speed


class Move(object):
    def __init__(self, robot_length, motor_left_port, motor_right_port):
        self.mdiff = MoveDifferential(motor_left_port, motor_right_port, EV3EducationSetTire, robot_length)
        time.sleep(0.1)

    def go_to_coords(self, speed, x, y, wait_until_not_moving=False):
        """
        Go to specified coordinates with specified speed (mm/s).
        Run a thread to move the robot while continuing execution of the program
        """
        thread = threading.Thread(target=self.__go_to_coordinates, args=(speed, x, y))
        thread.start()
        time.sleep(0.5)

        # Pause program while robot is moving
        if wait_until_not_moving:
            while thread.is_alive():
                time.sleep(0.01)

    def __go_to_coordinates(self, speed, x, y):
        speed_percent = SpeedTacho(speed).to_percentage(self.mdiff.left_motor)
        self.mdiff.on_to_coordinates(speed_percent, x, y)

    def slow_down(self, new_speed, x, y):
        self.stop()
        self.go_to_coords(new_speed, x, y)

    def go_for_distance(self, speed, distance_mm):
        speed_percent = SpeedTacho(speed).to_percentage(self.mdiff.left_motor)
        self.mdiff.on_for_distance(speed_percent, distance_mm)

    def turn_right(self, speed, degrees, use_gyro=False, error_margin=0):
        speed_percent = SpeedTacho(speed).to_percentage(self.mdiff.left_motor)
        self.mdiff.turn_right(speed_percent, degrees, use_gyro=use_gyro, error_margin=error_margin)

    def turn_left(self, speed, degrees, use_gyro=False, error_margin=0):
        speed_percent = SpeedTacho(speed).to_percentage(self.mdiff.left_motor)
        self.mdiff.turn_left(speed_percent, degrees, use_gyro=use_gyro, error_margin=error_margin)

    def stop(self):
        self.mdiff.left_motor.stop()
        self.mdiff.right_motor.stop()
