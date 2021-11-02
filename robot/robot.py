from robot.move import Move


class Robot(object):
    def __init__(self, robot_length, motor_ports=None):
        if "left" and "right" in motor_ports:
            self.move = Move(robot_length, motor_ports["left"], motor_ports["right"])






