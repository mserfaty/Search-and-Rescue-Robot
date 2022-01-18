#!/usr/bin/env python3
import time
from threading import Thread

from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D

from robot import Robot

sound = Sound()

# Robot properties
MOTOR_PORTS = {"wheel_right": OUTPUT_A, "pickup": OUTPUT_B, "wheel_left": OUTPUT_D}
SENSOR_PORTS = {"ultrasonic_sensor": INPUT_1, "metal_detector": INPUT_2, "gyro_sensor": INPUT_3,
                "color_sensor": INPUT_4}

ROBOT_LENGTH = 105.5  # 133.5  # 133.9

# Distances
DISTANCE_OBJECT = 200
SENSORS_DISTANCE = 45  # 70

# Speeds
NORMAL_SPEED = 200  # 20
AREA_SPEED = 170  # 15
TURNING_SPEED = 200
OBJECT_DETECTED_SPEED = 50  # 3
AVOID_SPEED = 100  # 10

# Tracks properties
TRACK_WIDTH = 50  # Width of the tracks for parallel track detection
PARALLEL_TRACK = True

# Object avoidance
skipcount = 0
object_avoided = False

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


def avoid_object():
    global object_avoided, skipcount
    robot.socket.reset_msg()

    # Go backward to avoid hitting object, then go to 3 TRACK_WIDTH mm on the right and continue track
    robot.move.go_for_distance(-AVOID_SPEED, 100)

    x = robot.move.mdiff.x_pos_mm + 3 * TRACK_WIDTH  # TODO: change nb 3
    y = robot.move.mdiff.y_pos_mm
    print((x, y), "AVOID")
    robot.move.go_to_coords(AVOID_SPEED, x, y, wait_until_not_moving=True)
    # detect_object((x, y))
    object_avoided = True

    # TODO: add other patterns
    if PARALLEL_TRACK:
        skipcount = 4


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
                time.sleep(0.5)

                # Detect if object is metallic or not
                if not robot.metal_detector.analog_read:
                    robot.socket.metal = 0  # Update message for GUI
                    sound.speak("Non metal object detected")
                    time.sleep(3)
                    avoid_object()
                    return

                # else:
                robot.socket.metal = 1  # Update message for GUI
                sound.speak("Metal object detected")
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
                        exit()

                    exit()
                    robot.move.go_for_distance(-AVOID_SPEED, 100)
                    time.sleep(1)
                    robot.move.go_to_coords(AREA_SPEED, x, y,
                                            wait_until_not_moving=True)  # TODO: Remember coords of avoided objects

                else:
                    avoid_object()
        time.sleep(0.05)


def execute_track(track):
    """Execute specified track and detect objects during execution"""
    global object_avoided, skipcount

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
    print("FINISHED")
    time.sleep(100)


def parallel_track_def():
    """Generate coordinates for parallel track with specified width between tracks"""

    # Create list of coordinates (Tuple) between 0 and 1000 mm
    track = [(x, y) for x in range(0, 1001, TRACK_WIDTH) for y in (0, 1000)]

    # Reorder list to have the parallel track
    try:
        for i in range(0, len(track), 4):
            track[i + 2], track[i + 3] = track[i + 3], track[i + 2]
    except IndexError:
        pass

    # Put Origin to last element of list
    track.append(track[0])
    track.pop(0)
    return track


if __name__ == '__main__':
    robot = Robot(ROBOT_LENGTH, MOTOR_PORTS, SENSOR_PORTS, GUI_ADDRESS)

    # parallel_track = [(0, 1100), (200, 1100), (200, 200), (400, 200),
    #                   (400, 1100), (600, 1100), (600, 200), (800, 200),
    #                   (800, 1100), (0, 0)]

    motor_mov_thread = Thread(target=check_for_motor_movement)
    motor_mov_thread.setDaemon(True)
    motor_mov_thread.start()

    if PARALLEL_TRACK:
        execute_track(parallel_track_def())
