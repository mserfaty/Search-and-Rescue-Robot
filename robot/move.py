import math
import _thread
import threading
import time
from logging import getLogger

from ev3dev2.motor import LargeMotor, SpeedNativeUnits, SpeedInvalid, MoveTank, MoveDifferential
from ev3dev2 import DeviceNotDefined, ThreadNotRunning
from ev3dev2.wheel import EV3EducationSetTire

# WHEEL_PERIMETER = 176  # Perimeter of the wheel in mm
SPEED_MODIFIER = 1
THRESHOLD_SPEED = 10
Kp = 27
Ki = 0.08
Kd = 1

log = getLogger(__name__)


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


class MoveDiff(object):
    def __init__(self, robot_length, motor_left_port, motor_right_port):
        self.mdiff = MoveDifferential(motor_left_port, motor_right_port, EV3EducationSetTire, robot_length)
        self.robot_wheels = EV3EducationSetTire()
        self.WHEEL_PERIMETER = self.robot_wheels.circumference_mm

        self.stop_thread = None

        self.dist_thread = None
        self.dist_proc = None

        self.speed_loop = None

        # self.speed_right_motor = []
        # self.pos_motors = []
        # self.last_error = 0
        # self.p = 0
        # self.i = 0
        # self.d = 0

        time.sleep(0.1)

    def go_straight(self, speed, distance, wait_until_not_moving=False):
        """
        :param speed: °/s
        :param distance: mm
        :param wait_until_not_moving: True or False
        :return:
        """
        self.stop_thread = False

        left_motor = LargeMotor(self.mdiff.left_motor.address)
        right_motor = LargeMotor(self.mdiff.right_motor.address)
        left_motor.reset()
        right_motor.reset()
        left_motor.speed_sp = speed
        right_motor.speed_sp = speed

        # self.mdiff.left_motor.reset()
        # self.mdiff.right_motor.reset()
        # print("LEFT_MOTOR_POSITION: ", self.mdiff.left_motor.position)
        # print("RIGHT_MOTOR_POSITION: ", self.mdiff.right_motor.position)
        # self.mdiff.left_motor.speed_sp = speed  # in °/s : 360°/s => self.WHEEL_PERIMETER (mm)/s
        # self.mdiff.right_motor.speed_sp = speed  # in °/s
        # print("LEFT_MOTOR_SPEED_SP: ", self.mdiff.left_motor.speed_sp)
        # print("RIGHT_MOTOR_SPEED_SP: ", self.mdiff.right_motor.speed_sp)
        time.sleep(0.01)

        left_motor.run_forever()
        right_motor.run_forever()
        # self.mdiff.left_motor.run_forever()
        # self.mdiff.right_motor.run_forever()

        # self.dist_proc = multiprocessing.Process(target=self.check_for_distance, args=(distance, speed))
        # self.dist_proc.start()
        self.dist_thread = threading.Thread(target=self.check_for_distance, args=(distance, speed, left_motor, right_motor))
        self.dist_thread.start()
        time.sleep(0.01)

        if wait_until_not_moving:
            while self.dist_thread.is_alive():
            # while self.dist_proc.is_alive():
                time.sleep(0.01)

        # self.write_to_file(self.pos_motors, self.speed_right_motor)

    def check_for_distance(self, distance, speed, left_motor, right_motor):
        total_degrees = distance / self.WHEEL_PERIMETER * 360
        self.speed_loop = speed

        while not self.stop_thread:
            # Robot has done wanted distance
            left_pos = left_motor.position
            # left_pos = self.mdiff.left_motor.position
            if left_pos > total_degrees:
                break

            # Compute error
            right_pos = right_motor.position
            # right_pos = self.mdiff.right_motor.position
            # self.pos_motors.append((left_pos, right_pos))
            error = right_pos - left_pos

            # Correct error  and adjust speed to go straight
            right_speed = SpeedNativeUnits(self.speed_loop).to_native_units(right_motor)
            # right_speed = SpeedNativeUnits(self.speed_loop).to_native_units(self.mdiff.right_motor)
            left_speed, right_speed = self.get_speed_steering(error, right_speed)  # TODO: ERROR
            self.change_speed(left_motor, left_speed)
            self.change_speed(right_motor, right_speed)
            # self.change_speed(self.mdiff.left_motor, left_speed)
            # self.change_speed(self.mdiff.right_motor, right_speed)
            # if abs(error) < SPEED_MODIFIER:  # No error
            #     time.sleep(0.01)
            #     continue
            # else:  # Error

            # speed_left = self.mdiff.left_motor.speed_sp
            # if error > 0 and speed_left - THRESHOLD_SPEED <= self.mdiff.right_motor.speed_sp - SPEED_MODIFIER <= speed_left + THRESHOLD_SPEED+5:
            #     self.change_speed(self.mdiff.right_motor, self.mdiff.right_motor.speed_sp - SPEED_MODIFIER)
            # else:
            #     if speed_left - THRESHOLD_SPEED <= self.mdiff.right_motor.speed_sp + SPEED_MODIFIER <= speed_left + THRESHOLD_SPEED+5:
            #         self.change_speed(self.mdiff.right_motor, self.mdiff.right_motor.speed_sp + SPEED_MODIFIER)
            # if error > 0:
            #     self.change_speed(self.mdiff.right_motor, self.mdiff.right_motor.speed_sp - SPEED_MODIFIER)
            # else:
            #     self.change_speed(self.mdiff.right_motor, self.mdiff.right_motor.speed_sp + SPEED_MODIFIER)

            time.sleep(0.01)

        left_motor.stop()
        right_motor.stop()
        # self.mdiff.left_motor.stop()
        # self.mdiff.right_motor.stop()

    def go_coord_straight(self, speed, x, y):
        self.mdiff.odometry_start()
        th = threading.Thread(target=self.__go_to_coordinates, args=(speed, x, y))
        th.start()
        # self.go_to_coordinates(speed, x, y)
        time.sleep(2)
        self.mdiff.left_motor.stop()
        self.mdiff.right_motor.stop()
        self.mdiff.odometry_thread_run = False
        self.mdiff.odometry_stop()

    # def check_for_distance(self, distance):
    #     total_degrees = distance / self.WHEEL_PERIMETER * 360
    #     while not self.stop_thread:
    #
    #         # Robot has done wanted distance
    #         left_pos = self.mdiff.left_motor.position
    #         if left_pos > total_degrees:
    #             break
    #
    #         # Correct error to go straight
    #         right_pos = self.mdiff.right_motor.position
    #         # error = right_pos - left_pos
    #         error = left_pos - right_pos
    #         print(error)
    #         # if abs(error) < SPEED_MODIFIER:  # No error
    #         #     time.sleep(0.01)
    #         #     continue
    #         # else:  # Error
    #         self.change_speed(self.mdiff.right_motor, self.compute_speed(error))
    #
    #             # speed_left = self.mdiff.left_motor.speed_sp
    #             # if error > 0 and speed_left - THRESHOLD_SPEED <= self.mdiff.right_motor.speed_sp - SPEED_MODIFIER <= speed_left + THRESHOLD_SPEED+5:
    #             #     self.change_speed(self.mdiff.right_motor, self.mdiff.right_motor.speed_sp - SPEED_MODIFIER)
    #             # else:
    #             #     if speed_left - THRESHOLD_SPEED <= self.mdiff.right_motor.speed_sp + SPEED_MODIFIER <= speed_left + THRESHOLD_SPEED+5:
    #             #         self.change_speed(self.mdiff.right_motor, self.mdiff.right_motor.speed_sp + SPEED_MODIFIER)
    #         # if error > 0:
    #         #     self.change_speed(self.mdiff.right_motor, self.mdiff.right_motor.speed_sp - SPEED_MODIFIER)
    #         # else:
    #         #     self.change_speed(self.mdiff.right_motor, self.mdiff.right_motor.speed_sp + SPEED_MODIFIER)
    #
    #         time.sleep(0.01)
    #
    #     self.mdiff.left_motor.stop()
    #     self.mdiff.right_motor.stop()

    @staticmethod
    def get_speed_steering(steering, speed):
        """
        Calculate the speed_sp for each motor in a pair to achieve the specified
        steering. Note that calling this function alone will not make the
        motors move, it only calculates the speed. A run_* function must be called
        afterwards to make the motors move.

        steering [-100, 100]:
            * -100 means turn left on the spot (right motor at 100% forward, left motor at 100% backward),
            *  0   means drive in a straight line, and
            *  100 means turn right on the spot (left motor at 100% forward, right motor at 100% backward).

        speed:
            The speed that should be applied to the outmost motor (the one
            rotating faster). The speed of the other motor will be computed
            automatically.
        """
        assert -100 <= steering <= 100, \
            "{} is an invalid steering, must be between -100 and 100 (inclusive)".format(steering)

        # We don't have a good way to make this generic for the pair... so we
        # assume that the left motor's speed stats are the same as the right motor's.
        left_speed = speed
        right_speed = speed
        speed_factor = (50 - abs(float(steering))) / 50
        if steering >= 0:
            right_speed *= speed_factor
        else:
            left_speed *= speed_factor

        return left_speed, right_speed

    def turn_right(self, speed, degrees, use_gyro=False, error_margin=0):
        speed_percent = SpeedTacho(speed).to_percentage(self.mdiff.left_motor)
        self.mdiff.turn_right(speed_percent, degrees, use_gyro=use_gyro, error_margin=error_margin)
        # self.mdiff.turn_right(speed, degrees)

    def turn_left(self, speed, degrees, use_gyro=False, error_margin=0):
        speed_percent = SpeedTacho(speed).to_percentage(self.mdiff.left_motor)
        self.mdiff.turn_left(speed_percent, degrees, use_gyro=use_gyro, error_margin=error_margin)
        # self.mdiff.turn_left(speed, degrees)

    def go_for_distance(self, speed, distance_mm):
        speed_percent = SpeedTacho(speed).to_percentage(self.mdiff.left_motor)
        self.mdiff.on_for_distance(speed_percent, distance_mm)

    def go_to_coords(self, speed, x, y, wait_until_not_moving=False):
        self.dist_thread = threading.Thread(target=self.__go_to_coordinates, args=(speed, x, y))
        self.dist_thread.start()
        time.sleep(0.5)
        if wait_until_not_moving:
            while self.dist_thread.is_alive():
                time.sleep(0.01)

    def __go_to_coordinates(self, speed, x, y):
        speed_percent = SpeedTacho(speed).to_percentage(self.mdiff.left_motor)
        self.mdiff.on_to_coordinates(speed_percent, x, y)

    def slow_down(self, speed, x, y):
        self.stop()
        self.go_to_coords(speed, x, y)

    def stop(self):
        self.mdiff.left_motor.stop()
        self.mdiff.right_motor.stop()

    def stop_motors(self):
        if self.dist_thread is not None and self.dist_thread.is_alive:
            self.stop_thread = True
            self.dist_thread.join()
        # if self.dist_proc is not None and self.dist_proc.is_alive:
        #     self.stop_thread = True
        #     self.dist_proc.join()
        # self.dist_proc.terminate()

    @staticmethod
    def change_speed(motor, new_speed):
        # current_speed = motor.speed_sp
        # self.speed_right_motor.append((current_speed, new_speed))
        motor.speed_sp = new_speed
        motor.run_forever()

    # DEBUGGING
    @staticmethod
    def write_to_file(position_motors, speed_right_motor):
        with open("./speed_motor.txt", "w") as speed_motor:
            for element in speed_right_motor:
                speed_motor.write("%s\n" % str(element))
        with open("./pos_motors.txt", "w") as pos_motors:
            for element in position_motors:
                pos_motors.write("%s\n" % str(element))


# ==== Old Code with MoveDifferential and Move classes ====
class MoveDifferentialBis(MoveTank):
    """
    MoveDifferential is a child of MoveTank that adds the following capabilities:

    - drive in a straight line for a specified distance

    - rotate in place in a circle (clockwise or counter clockwise) for a
      specified number of degrees

    - drive in an arc (clockwise or counter clockwise) of a specified radius
      for a specified distance

    Odometry can be use to enable driving to specific coordinates and
    rotating to a specific angle.

    New arguments:

    wheel_class - Typically a child class of :class:`ev3dev2.wheel.Wheel`. This is used to
    get the circumference of the wheels of the robot. The circumference is
    needed for several calculations in this class.

    wheel_distance_mm - The distance between the mid point of the two
    wheels of the robot. You may need to do some test drives to find
    the correct value for your robot.  It is not as simple as measuring
    the distance between the midpoints of the two wheels. The weight of
    the robot, center of gravity, etc come into play.

    You can use utils/move_differential.py to call on_arc_left() to do
    some test drives of circles with a radius of 200mm. Adjust your
    wheel_distance_mm until your robot can drive in a perfect circle
    and stop exactly where it started. It does not have to be a circle
    with a radius of 200mm, you can test with any size circle but you do
    not want it to be too small or it will be difficult to test small
    adjustments to wheel_distance_mm.

    Example:

    .. code:: python

        from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveDifferential, SpeedRPM
        from ev3dev2.wheel import EV3Tire

        STUD_MM = 8

        # test with a robot that:
        # - uses the standard wheels known as EV3Tire
        # - wheels are 16 studs apart
        mdiff = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3Tire, 16 * STUD_MM)

        # Rotate 90 degrees clockwise
        mdiff.turn_right(SpeedRPM(40), 90)

        # Drive forward 500 mm
        mdiff.on_for_distance(SpeedRPM(40), 500)

        # Drive in arc to the right along an imaginary circle of radius 150 mm.
        # Drive for 700 mm around this imaginary circle.
        mdiff.on_arc_right(SpeedRPM(80), 150, 700)

        # Enable odometry
        mdiff.odometry_start()

        # Use odometry to drive to specific coordinates
        mdiff.on_to_coordinates(SpeedRPM(40), 300, 300)

        # Use odometry to go back to where we started
        mdiff.on_to_coordinates(SpeedRPM(40), 0, 0)

        # Use odometry to rotate in place to 90 degrees
        mdiff.turn_to_angle(SpeedRPM(40), 90)

        # Disable odometry
        mdiff.odometry_stop()
    """
    def __init__(self,
                 left_motor_port,
                 right_motor_port,
                 wheel_class,
                 wheel_distance_mm,
                 desc=None,
                 motor_class=LargeMotor):

        MoveTank.__init__(self, left_motor_port, right_motor_port, desc, motor_class)
        self.wheel = wheel_class()
        self.wheel_distance_mm = wheel_distance_mm

        # The circumference of the circle made if this robot were to rotate in place
        self.circumference_mm = self.wheel_distance_mm * math.pi

        self.min_circle_radius_mm = self.wheel_distance_mm / 2

        # odometry variables
        self.x_pos_mm = 0.0  # robot X position in mm
        self.y_pos_mm = 0.0  # robot Y position in mm
        self.odometry_thread_run = False
        self.theta = 0.0

    def on_for_distance(self, speed, distance_mm, brake=True, block=True):
        """
        Drive in a straight line for ``distance_mm``
        """
        rotations = distance_mm / self.wheel.circumference_mm
        log.debug("%s: on_for_rotations distance_mm %s, rotations %s, speed %s" % (self, distance_mm, rotations, speed))

        MoveTank.on_for_rotations(self, speed, speed, rotations, brake, block)

    def _on_arc(self, speed, radius_mm, distance_mm, brake, block, arc_right):
        """
        Drive in a circle with 'radius' for 'distance'
        """

        if radius_mm < self.min_circle_radius_mm:
            raise ValueError("{}: radius_mm {} is less than min_circle_radius_mm {}".format(
                self, radius_mm, self.min_circle_radius_mm))

        # The circle formed at the halfway point between the two wheels is the
        # circle that must have a radius of radius_mm
        circle_outer_mm = 2 * math.pi * (radius_mm + (self.wheel_distance_mm / 2))
        circle_middle_mm = 2 * math.pi * radius_mm
        circle_inner_mm = 2 * math.pi * (radius_mm - (self.wheel_distance_mm / 2))

        if arc_right:
            # The left wheel is making the larger circle and will move at 'speed'
            # The right wheel is making a smaller circle so its speed will be a fraction of the left motor's speed
            left_speed = speed
            right_speed = float(circle_inner_mm / circle_outer_mm) * left_speed

        else:
            # The right wheel is making the larger circle and will move at 'speed'
            # The left wheel is making a smaller circle so its speed will be a fraction of the right motor's speed
            right_speed = speed
            left_speed = float(circle_inner_mm / circle_outer_mm) * right_speed

        log.debug("%s: arc %s, radius %s, distance %s, left-speed %s, right-speed %s" %
                  (self, "right" if arc_right else "left", radius_mm, distance_mm, left_speed, right_speed))
        log.debug("%s: circle_outer_mm %s, circle_middle_mm %s, circle_inner_mm %s" %
                  (self, circle_outer_mm, circle_middle_mm, circle_inner_mm))

        # We know we want the middle circle to be of length distance_mm so
        # calculate the percentage of circle_middle_mm we must travel for the
        # middle of the robot to travel distance_mm.
        circle_middle_percentage = float(distance_mm / circle_middle_mm)

        # Now multiple that percentage by circle_outer_mm to calculate how
        # many mm the outer wheel should travel.
        circle_outer_final_mm = circle_middle_percentage * circle_outer_mm

        outer_wheel_rotations = float(circle_outer_final_mm / self.wheel.circumference_mm)
        outer_wheel_degrees = outer_wheel_rotations * 360

        log.debug("%s: arc %s, circle_middle_percentage %s, circle_outer_final_mm %s, " %
                  (self, "right" if arc_right else "left", circle_middle_percentage, circle_outer_final_mm))
        log.debug("%s: outer_wheel_rotations %s, outer_wheel_degrees %s" %
                  (self, outer_wheel_rotations, outer_wheel_degrees))

        MoveTank.on_for_degrees(self, left_speed, right_speed, outer_wheel_degrees, brake, block)

    def on_arc_right(self, speed, radius_mm, distance_mm, brake=True, block=True):
        """
        Drive clockwise in a circle with 'radius_mm' for 'distance_mm'
        """
        self._on_arc(speed, radius_mm, distance_mm, brake, block, True)

    def on_arc_left(self, speed, radius_mm, distance_mm, brake=True, block=True):
        """
        Drive counter-clockwise in a circle with 'radius_mm' for 'distance_mm'
        """
        self._on_arc(speed, radius_mm, distance_mm, brake, block, False)

    def turn_degrees(self, speed, degrees, brake=True, block=True, error_margin=2, use_gyro=False):
        """
        Rotate in place ``degrees``. Both wheels must turn at the same speed for us
        to rotate in place.  If the following conditions are met the GryoSensor will
        be used to improve the accuracy of our turn:
        - ``use_gyro``, ``brake`` and ``block`` are all True
        - A GyroSensor has been defined via ``self.gyro = GyroSensor()``
        """
        def final_angle(init_angle, degrees):
            result = init_angle - degrees

            while result <= -360:
                result += 360

            while result >= 360:
                result -= 360

            if result < 0:
                result += 360

            return result

        # use the gyro to check that we turned the correct amount?
        use_gyro = bool(use_gyro and block and brake)
        if use_gyro and not self._gyro:
            raise DeviceNotDefined(
                "The 'gyro' variable must be defined with a GyroSensor. Example: tank.gyro = GyroSensor()")

        if use_gyro:
            angle_init_degrees = self._gyro.circle_angle()
        else:
            angle_init_degrees = math.degrees(self.theta)

        angle_target_degrees = final_angle(angle_init_degrees, degrees)

        log.info("%s: turn_degrees() %d degrees from %s to %s" %
                 (self, degrees, angle_init_degrees, angle_target_degrees))

        # The distance each wheel needs to travel
        distance_mm = (abs(degrees) / 360) * self.circumference_mm

        # The number of rotations to move distance_mm
        rotations = distance_mm / self.wheel.circumference_mm

        # If degrees is positive rotate clockwise
        if degrees > 0:
            MoveTank.on_for_rotations(self, speed, speed * -1, rotations, brake, block)

        # If degrees is negative rotate counter-clockwise
        else:
            MoveTank.on_for_rotations(self, speed * -1, speed, rotations, brake, block)

        if use_gyro:
            angle_current_degrees = self._gyro.circle_angle()

            # This can happen if we are aiming for 2 degrees and overrotate to 358 degrees
            # We need to rotate counter-clockwise
            if 90 >= angle_target_degrees >= 0 and 270 <= angle_current_degrees <= 360:
                degrees_error = (angle_target_degrees + (360 - angle_current_degrees)) * -1

            # This can happen if we are aiming for 358 degrees and overrotate to 2 degrees
            # We need to rotate clockwise
            elif 360 >= angle_target_degrees >= 270 and 0 <= angle_current_degrees <= 90:
                degrees_error = angle_current_degrees + (360 - angle_target_degrees)

            # We need to rotate clockwise
            elif angle_current_degrees > angle_target_degrees:
                degrees_error = angle_current_degrees - angle_target_degrees

            # We need to rotate counter-clockwise
            else:
                degrees_error = (angle_target_degrees - angle_current_degrees) * -1

            log.info("%s: turn_degrees() ended up at %s, error %s, error_margin %s" %
                     (self, angle_current_degrees, degrees_error, error_margin))

            if abs(degrees_error) > error_margin:
                self.turn_degrees(speed, degrees_error, brake, block, error_margin, use_gyro)

    def turn_right(self, speed, degrees, brake=True, block=True, error_margin=2, use_gyro=False):
        """
        Rotate clockwise ``degrees`` in place
        """
        self.turn_degrees(speed, abs(degrees), brake, block, error_margin, use_gyro)

    def turn_left(self, speed, degrees, brake=True, block=True, error_margin=2, use_gyro=False):
        """
        Rotate counter-clockwise ``degrees`` in place
        """
        self.turn_degrees(speed, abs(degrees) * -1, brake, block, error_margin, use_gyro)

    def turn_to_angle(self, speed, angle_target_degrees, brake=True, block=True, error_margin=2, use_gyro=False):
        """
        Rotate in place to ``angle_target_degrees`` at ``speed``
        """
        if not self.odometry_thread_run:
            raise ThreadNotRunning("odometry_start() must be called to track robot coordinates")

        # Make both target and current angles positive numbers between 0 and 360
        while angle_target_degrees < 0:
            angle_target_degrees += 360

        angle_current_degrees = math.degrees(self.theta)

        while angle_current_degrees < 0:
            angle_current_degrees += 360

        # Is it shorter to rotate to the right or left
        # to reach angle_target_degrees?
        if angle_current_degrees > angle_target_degrees:
            turn_right = True
            angle_delta = angle_current_degrees - angle_target_degrees
        else:
            turn_right = False
            angle_delta = angle_target_degrees - angle_current_degrees

        # if angle_delta > 180:
        #     angle_delta = 360 - angle_delta
        #     turn_right = not turn_right

        log.debug("%s: turn_to_angle %s, current angle %s, delta %s, turn_right %s" %
                  (self, angle_target_degrees, angle_current_degrees, angle_delta, turn_right))
        self.odometry_coordinates_log()

        if turn_right:
            self.turn_degrees(speed, abs(angle_delta), brake, block, error_margin, use_gyro)
        else:
            self.turn_degrees(speed, abs(angle_delta) * -1, brake, block, error_margin, use_gyro)
            # self.turn_degrees(speed, 360 - abs(angle_delta) * 1, brake, block, error_margin, use_gyro)

        self.odometry_coordinates_log()

    def odometry_coordinates_log(self):
        log.debug("%s: odometry angle %s at (%d, %d)" % (self, math.degrees(self.theta), self.x_pos_mm, self.y_pos_mm))

    def odometry_start(self, theta_degrees_start=90.0, x_pos_start=0.0, y_pos_start=0.0, sleep_time=0.005):  # 5ms
        """
        Ported from:
        http://seattlerobotics.org/encoder/200610/Article3/IMU%20Odometry,%20by%20David%20Anderson.htm

        A thread is started that will run until the user calls odometry_stop()
        which will set odometry_thread_run to False
        """
        def _odometry_monitor():
            left_previous = 0
            right_previous = 0
            self.theta = math.radians(theta_degrees_start)  # robot heading
            self.x_pos_mm = x_pos_start  # robot X position in mm
            self.y_pos_mm = y_pos_start  # robot Y position in mm
            TWO_PI = 2 * math.pi
            self.odometry_thread_run = True

            while self.odometry_thread_run:

                # sample the left and right encoder counts as close together
                # in time as possible
                left_current = self.left_motor.position
                right_current = self.right_motor.position

                # determine how many ticks since our last sampling
                left_ticks = left_current - left_previous
                right_ticks = right_current - right_previous

                # Have we moved?
                if not left_ticks and not right_ticks:
                    if sleep_time:
                        time.sleep(sleep_time)
                    continue

                # update _previous for next time
                left_previous = left_current
                right_previous = right_current

                # rotations = distance_mm/self.wheel.circumference_mm
                left_rotations = float(left_ticks / self.left_motor.count_per_rot)
                right_rotations = float(right_ticks / self.right_motor.count_per_rot)

                # convert longs to floats and ticks to mm
                left_mm = float(left_rotations * self.wheel.circumference_mm)
                right_mm = float(right_rotations * self.wheel.circumference_mm)

                # calculate distance we have traveled since last sampling
                mm = (left_mm + right_mm) / 2.0

                # accumulate total rotation around our center
                self.theta += (right_mm - left_mm) / self.wheel_distance_mm

                # and clip the rotation to plus or minus 360 degrees
                self.theta -= float(int(self.theta / TWO_PI) * TWO_PI)

                # now calculate and accumulate our position in mm
                self.x_pos_mm += mm * math.cos(self.theta)
                self.y_pos_mm += mm * math.sin(self.theta)

                if sleep_time:
                    time.sleep(sleep_time)

        _thread.start_new_thread(_odometry_monitor, ())

        # Block until the thread has started doing work
        while not self.odometry_thread_run:
            pass

    def odometry_stop(self):
        """
        Signal the odometry thread to exit
        """

        if self.odometry_thread_run:
            self.odometry_thread_run = False

    def on_to_coordinates(self, speed, x_target_mm, y_target_mm, brake=True, block=True):
        """
        Drive to (``x_target_mm``, ``y_target_mm``) coordinates at ``speed``
        """
        if not self.odometry_thread_run:
            raise ThreadNotRunning("odometry_start() must be called to track robot coordinates")

        # stop moving
        self.off(brake='hold')

        # rotate in place so we are pointed straight at our target
        x_delta = x_target_mm - self.x_pos_mm
        y_delta = y_target_mm - self.y_pos_mm
        angle_target_radians = math.atan2(y_delta, x_delta)
        angle_target_degrees = math.degrees(angle_target_radians)
        self.turn_to_angle(speed, angle_target_degrees, brake=True, block=True)

        # drive in a straight line to the target coordinates
        distance_mm = math.sqrt(pow(self.x_pos_mm - x_target_mm, 2) + pow(self.y_pos_mm - y_target_mm, 2))
        self.on_for_distance(speed, distance_mm, brake, block)


class Move(object):
    def __init__(self, robot_length, motor_left_port, motor_right_port):
        self.left_motor = LargeMotor(motor_left_port)
        # self.left_motor.reset()
        self.right_motor = LargeMotor(motor_right_port)
        # self.right_motor.reset()

        self.robot_wheels = EV3EducationSetTire()
        self.WHEEL_PERIMETER = self.robot_wheels.circumference_mm
        self.robot_length = robot_length
        time.sleep(0.1)

    def go_straight(self, speed, distance):
        self.left_motor.reset()
        self.right_motor.reset()

        self.left_motor.speed_sp = speed
        self.right_motor.speed_sp = speed
        time.sleep(0.1)
        self.left_motor.run_forever()
        self.right_motor.run_forever()

        while self.left_motor.position < (distance / self.WHEEL_PERIMETER * 360):
            pass

        self.left_motor.stop()
        self.right_motor.stop()

    def _turn(self, speed, degrees):
        self.left_motor.reset()
        self.right_motor.reset()

        # The distance each wheel needs to travel
        distance_mm = (abs(degrees) / 360) * self.robot_length

        # The number of rotations to move distance_mm
        rotations = distance_mm / self.WHEEL_PERIMETER

        # If degrees is positive rotate clockwise
        if degrees > 0:
            self.left_motor.on_for_rotations(speed, rotations, block=False)
            self.right_motor.on_for_rotations(speed * -1, rotations, block=False)

        # If degrees is negative rotate counter-clockwise
        else:
            self.left_motor.on_for_rotations(speed * -1, rotations, block=False)
            self.right_motor.on_for_rotations(speed, rotations, block=False)

    def turn_left(self, speed, degrees):
        self._turn(speed, abs(degrees) * -1)

    def turn_right(self, speed, degrees):
        self._turn(speed, abs(degrees))
