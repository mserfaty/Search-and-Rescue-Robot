#!/usr/bin/env python3

from time import sleep

# from ev3dev2._platform.ev3 import INPUT_3
from ev3dev2.motor import OUTPUT_A, LargeMotor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound


class Motor(object):

    #    def __init__(self, motor_port=OUTPUT_A, color_sensor_port=INPUT_3, drive_speed_pct=60):
    def __init__(self, motor_port=OUTPUT_A):

        self.motor = LargeMotor(motor_port)
        self.speaker = Sound()

        self.STEER_SPEED_PCT = 30

        self.sensor = ColorSensor()

    def color_sensor(self):
        while True:
            color = self.sensor.color
            text = ColorSensor.COLORS[color]
            self.speaker.speak(text)
            if text == "Red":
                self.make_move(self.motor, self.STEER_SPEED_PCT)
            sleep(2)
            self.stop_motor(self.motor)

            sleep(4)

    def make_move(self, motor, speed):
        motor.on(speed)

    def stop_motor(self, motor,):
        motor.stop()


if __name__ == '__main__':

    robot = Motor()
    robot.color_sensor()
