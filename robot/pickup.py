import time

from ev3dev2.motor import MediumMotor

TIMEOUT_ARM = 30


class Pickup(object):
    def __init__(self, motor_left_port, motor_right_port):
        self.left_motor = MediumMotor(motor_left_port)
        self.right_motor = MediumMotor(motor_right_port)
        time.sleep(0.1)
        self.initialize_arms()

    def initialize_arms(self):
        self.move_arm(self.left_motor, 100, -400)
        self.move_arm(self.right_motor, 100, 400)
        time.sleep(1)
        self.left_motor.reset()
        time.sleep(0.1)
        self.right_motor.reset()
        time.sleep(0.1)
        self.open_for_detection()

    @staticmethod
    def move_arm(motor, speed, degrees):
        motor.speed_sp = speed
        time.sleep(0.1)
        motor.position_sp = degrees
        time.sleep(0.1)
        motor.run_to_abs_pos()

    def open_arms(self):
        """anti-clockwise"""
        self.move_arm(self.left_motor, 100, 60)
        self.move_arm(self.right_motor, 100, -60)
        self.left_motor.wait_until_not_moving(TIMEOUT_ARM)
        self.right_motor.wait_until_not_moving(TIMEOUT_ARM)
        time.sleep(2)

    def close_arms(self):
        """clockwise"""
        self.move_arm(self.left_motor, 100, 170)
        self.move_arm(self.right_motor, 100, -170)
        self.left_motor.wait_until_not_moving(TIMEOUT_ARM)
        self.right_motor.wait_until_not_moving(TIMEOUT_ARM)
        time.sleep(2)

    def open_for_detection(self):
        """anti-clockwise"""
        self.move_arm(self.left_motor, 100, 35)
        self.move_arm(self.right_motor, 100, -35)
        self.left_motor.wait_until_not_moving(TIMEOUT_ARM)
        self.right_motor.wait_until_not_moving(TIMEOUT_ARM)
        time.sleep(2)
