#!/usr/bin/env python3
import time
import threading

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, LargeMotor


class Robot(object):
    def __init__(self, motor_right_port=OUTPUT_B, motor_left_port=OUTPUT_A):
        self.motor_right = LargeMotor(motor_right_port)
        self.motor_left = LargeMotor(motor_left_port)
        self.degrees = 360*5

    def main(self):
        """
        Execute a Motor loop
        """
        # self.motor_left.on(100)
        # self.motor_right.on(100)

        # threading.Thread(target=self.motor_left.on_for_degrees, args=(50, self.degrees)).start()
        # self.motor_right.on_for_degrees(50, self.degrees)
        # time.sleep(1)

        # (0, 360*2.7) (90, 1062)
        threading.Thread(target=self.motor_left.on_for_degrees, args=(100, 90)).start()
        self.motor_right.on_for_degrees(50, 1062)

        # time.sleep(1)
        # threading.Thread(target=self.motor_left.on_for_degrees, args=(50, self.degrees)).start()
        # self.motor_right.on_for_degrees(50, self.degrees)

        time.sleep(3)

        print(self.motor_left.position)
        print(self.motor_right.position)

        self.motor_right.reset()
        self.motor_left.reset()


if __name__ == '__main__':
    robot = Robot()  # Initialisation of the robot
    robot.main()  # Execution of the Motor loop
