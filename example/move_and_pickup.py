#!/usr/bin/env python3
import time
from threading import Thread

from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D

from robot import Robot
from robot.patterns import SpiralPattern, ParallelTrack

sound = Sound()

# Robot properties
MOTOR_PORTS = {"wheel_right": OUTPUT_A, "pickup": OUTPUT_B, "wheel_left": OUTPUT_D}
SENSOR_PORTS = {"ultrasonic_sensor": INPUT_1, "metal_detector": INPUT_2, "gyro_sensor": INPUT_3,
                "color_sensor": INPUT_4}

ROBOT_LENGTH = 135
ROBOT_LENGTH_SIDE = 125.5
ROBOT_LENGTH_SPIRAL = 135

# Distances
DISTANCE_OBJECT = 200
SENSORS_DISTANCE = 45  # 70

# Speeds
NORMAL_SPEED = 200  # 20
AREA_SPEED = 170  # 15
TURNING_SPEED = 200
OBJECT_DETECTED_SPEED = 50  # 3
AVOID_SPEED = 100  # 10

# Patterns properties
PATTERN_WIDTH = 200  # Width of the tracks for parallel track detection

# Selection of wanted pattern (put one to "True", all others to "False")
PARALLEL_PATTERN_FRONT = True
PARALLEL_PATTERN_SIDE = False
SPIRAL_PATTERN = False

# Pickup
pickup_priority = ["Blue", "Black"]

# Communication with GUI
GUI_ADDRESS = {"host": "172.20.10.3", "port": 5204}


def check_for_motor_movement():
    while True:
        if robot.move.mdiff.left_motor.is_running or robot.move.mdiff.right_motor.is_running:
            robot.socket.in_movement = 1
        else:
            robot.socket.in_movement = 0
        time.sleep(0.01)


def pick_object():
    robot.pickup.close_arms()
    time.sleep(2)
    robot.socket.picked_up = 1


def release_object():
    robot.pickup.open_arms()
    time.sleep(2)
    robot.socket.dropped = 1


def go_back():
    robot.socket.sensed_object = 0
    robot.socket.metal = -1
    robot.move.go_to_coords(AREA_SPEED, 0, 0, wait_until_not_moving=True)


def define_increasing_axis(current_coords, cmd_coords):
    """
    Define which axis of x or y is increasing for avoiding object
    
    :param current_coords: current position of robot (Tuple[int, int])
    :param cmd_coords: command where the robot were going before detecting an object (Tuple[int, int])
    :return: "x" of "y" (str)
    """
    delta_x = abs(cmd_coords[0] - current_coords[0])
    delta_y = abs(cmd_coords[1] - current_coords[1])
    if max(delta_x, delta_y) == delta_x:
        return "x"
    else:
        return "y"


def avoid_object(cmd_x, cmd_y):
    robot.socket.reset_msg()

    # Go backward to avoid hitting object
    robot.move.go_for_distance(-AVOID_SPEED, 100)

    # Get around the object to avoid it
    current_coords = (robot.move.mdiff.x_pos_mm, robot.move.mdiff.y_pos_mm)
    increasing_axis = define_increasing_axis(current_coords, (cmd_x, cmd_y))
    if PARALLEL_PATTERN_FRONT or PARALLEL_PATTERN_SIDE or SPIRAL_PATTERN:
        if increasing_axis == "x":  # Side
            x = current_coords[0]
            y = current_coords[1] + 1 * PATTERN_WIDTH
        else:  # Front
            x = current_coords[0] + 1 * PATTERN_WIDTH
            y = current_coords[1]
    else:
        raise ValueError("No pattern specified")
    robot.move.go_to_coords(AVOID_SPEED, x, y, wait_until_not_moving=True)
    # detect_object((x, y))
    object_avoided = True

    # Continue track
    if SPIRAL_PATTERN:
        if increasing_axis == "x":  # Side
            robot.move.go_to_coords(AVOID_SPEED, x, cmd_y)
            detect_object((x, cmd_y))
        else:  # Front
            robot.move.go_to_coords(AVOID_SPEED, cmd_x, y)
            detect_object((cmd_x, y))


def detect_object(destination_coords):
    """Detect and discriminate objects and pick or avoid them"""
    global pickup_priority

    x = destination_coords[0]  # TODO: delete
    y = destination_coords[1]  # TODO: delete

    has_slowed_down = False
    while robot.move.dist_thread.is_alive():
        distance_object = robot.ultrasonic_sensor.value()  # Retrieve distance of object from ultrasonic sensor

        # Object detected at less than DISTANCE_OBJECT cm
        if distance_object < DISTANCE_OBJECT:
            robot.socket.sensed_object = 1

            # Slow down the robot to avoid hitting the object
            if not has_slowed_down:
                has_slowed_down = True
                robot.move.slow_down(OBJECT_DETECTED_SPEED, x, y)

            # Object is in range of metal detector
            if distance_object < SENSORS_DISTANCE:
                robot.move.stop()
                time.sleep(1)

                # Detect if object is metallic or not
                if not robot.metal_detector.analog_read:
                    sound.speak("Non metal object detected")
                    time.sleep(0.5)
                    robot.socket.metal = 0  # Update message for GUI
                    time.sleep(3)
                    avoid_object(x, y)
                    return

                else:
                    sound.speak("Metal object detected")
                    time.sleep(0.5)
                    robot.socket.metal = 1  # Update message for GUI
                    time.sleep(2)

                    # Sense color of object and handle it according to set priority
                    # TODO: color with RGB
                    detected_color = robot.color_sensor.COLORS[robot.color_sensor.color]
                    # detected_color = robot.color_sensor.color_name
                    # print(detected_color)
                    txt = "{0} object detected".format(detected_color)
                    sound.speak(txt)
                    # detected_color = robot.color_sensor.rgb
                    robot.socket.color = robot.color_sensor.rgb  # TODO

                    # No priority has been decided
                    try:
                        if not pickup_priority:  # None or empty
                            pick_object()
                            go_back()
                            release_object()
                    except NameError:
                        pick_object()
                        go_back()
                        release_object()

                    # Object is number 1 priority
                    if detected_color == pickup_priority[0]:
                        pick_object()
                        go_back()
                        release_object()
                        pickup_priority.pop(0)  # Remove object from priority list

                        # List is empty so all objects have been taken
                        if not pickup_priority:
                            time.sleep(3)
                            exit()

                        time.sleep(3)
                        exit()

                        robot.move.go_for_distance(-AVOID_SPEED, 100)
                        time.sleep(1)
                        robot.move.go_to_coords(AREA_SPEED, x, y,
                                                wait_until_not_moving=True)  # TODO: Remember coords of avoided objects
                    else:
                        avoid_object(x, y)
        time.sleep(0.05)


def execute_pattern(track):
    """Execute specified pattern and detect objects during execution"""
    robot.move.mdiff.odometry_start()  # Start odometry to track coordinates of the robot

    # Go to each pair of coordinates in the list while detecting potential objects
    for coords in track:
        if skipcount > 0:
            # print(coords, "SKIPPED")
            skipcount -= 1
            continue

        if object_avoided:
            object_avoided = False

        # print(coords)
        robot.move.go_to_coords(AREA_SPEED, coords[0], coords[1])
        time.sleep(0.01)
        detect_object(coords)

    robot.move.mdiff.odometry_stop()  # When track is finished, stop tracking coordinates


if __name__ == '__main__':
    # Instantiate a Robot object
    if PARALLEL_PATTERN_FRONT:
        robot = Robot(ROBOT_LENGTH, MOTOR_PORTS, SENSOR_PORTS, GUI_ADDRESS)
    elif PARALLEL_PATTERN_SIDE:
        robot = Robot(ROBOT_LENGTH_SIDE, MOTOR_PORTS, SENSOR_PORTS, GUI_ADDRESS)
    elif SPIRAL_PATTERN:
        robot = Robot(ROBOT_LENGTH_SPIRAL, MOTOR_PORTS, SENSOR_PORTS, GUI_ADDRESS)

    # parallel_track = [(0, 1100), (200, 1100), (200, 200), (400, 200),
    #                   (400, 1100), (600, 1100), (600, 200), (800, 200),
    #                   (800, 1100), (0, 0)]

    motor_mov_thread = Thread(target=check_for_motor_movement)
    motor_mov_thread.setDaemon(True)
    motor_mov_thread.start()

    # Execute pattern
    if PARALLEL_PATTERN_FRONT:
        execute_pattern(ParallelTrack(parallel_pattern_front=True, track_width=PATTERN_WIDTH).pattern)
    if PARALLEL_PATTERN_SIDE:
        execute_pattern(ParallelTrack(parallel_pattern_side=True, track_width=PATTERN_WIDTH).pattern)
    if SPIRAL_PATTERN:
        execute_pattern(SpiralPattern(PATTERN_WIDTH).pattern)
