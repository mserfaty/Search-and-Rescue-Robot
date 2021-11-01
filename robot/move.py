from ev3dev2.motor import MoveDifferential
from ev3dev2.wheel import EV3EducationSetTire

WHEEL_PERIMETER = 176  # Perimeter of the wheel in mm


class Move(object):
    def __init__(self, robot_length, motor_left_port, motor_right_port):
        # self.tank = MoveTank(motor_left_port, motor_right_port)
        # self.motor_left = LargeMotor(motor_left_port)
        # self.motor_right = LargeMotor(motor_right_port)
        # self.degrees = 360*5
        self.mdiff = MoveDifferential(motor_left_port, motor_right_port, EV3EducationSetTire, robot_length)

    def go_straight(self, speed, distance):
        """
        :param speed: between 0 and 100
        :param distance: in mm
        """
        degrees = distance / WHEEL_PERIMETER * 360
        self.mdiff.on_for_degrees(speed, speed, degrees)

    def turn_right(self, speed, degrees):
        self.mdiff.turn_right(speed, degrees)

    def turn_left(self, speed, degrees):
        self.mdiff.turn_left(speed, degrees)
