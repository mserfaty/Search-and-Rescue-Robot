"""
License: You are free to use any part of code in this project as long as you mention original authors of this program:
Alpha Team composed of: Nirmalraj JEYANATHAN Joseph - SERFATY Milan - YE Hang - ZHANG Yujia

Supervised by Aurore (aurore.isep@gmail.com) and Hugo (myrobotswillconquertheworld@gmail.com)
IE.3510 (System Modeling) - ISEP 2022
"""

import time
from socket import socket
from threading import Thread


class Client:
    """
    Communication for GUI (client/Lego side)
    """

    def __init__(self, host='', port=5204):
        self.socket = socket()
        self.host = host
        self.port = port

        self.reset_msg()  # Data to send

        self._is_connected = False
        self._connect()

    def _connect(self):
        self.socket.connect((self.host, self.port))
        self._is_connected = True

        # Start sending messages to server
        thread = Thread(target=self._send_msg)
        thread.setDaemon(True)
        thread.start()

    def disconnect(self):
        self._is_connected = False

    def _send_msg(self):
        previous_msg = 0
        while self._is_connected:
            try:
                if self._msg_to_send != previous_msg:
                    self.socket.send(self.parse_msg().encode())
                    previous_msg = self._msg_to_send.copy()
            except Exception:
                print("Error occurred while sending message")
            time.sleep(0.01)
        self.socket.close()

    def parse_msg(self):
        """
        Parse list of values to a single message
        ex: from [0, 0, -1, (0, 0, 0), 0, 0] to "0\n0\n-1\n0\n0\n0\n0\n0"
        """

        message = ""
        for value in self._msg_to_send:
            if isinstance(value, int):
                message += str(value) + "\n"
            elif isinstance(value, tuple):
                for i in value:
                    message += str(i) + "\n"
        return message

    def reset_msg(self):
        # in_movement, sensed_object, metal, color, picked_up, dropped
        self._msg_to_send = [0, 0, -1, (0, 0, 0), 0, 0]

    @property
    def in_movement(self):
        return self._msg_to_send[0]

    @in_movement.setter
    def in_movement(self, value):
        if value in (0, 1):
            self._msg_to_send[0] = value

    @property
    def sensed_object(self):
        return self._msg_to_send[1]

    @sensed_object.setter
    def sensed_object(self, value):
        if value in (0, 1):
            self._msg_to_send[1] = value

    @property
    def metal(self):
        return self._msg_to_send[2]

    @metal.setter
    def metal(self, value):
        if value in (0, 1, 2):
            self._msg_to_send[2] = value

    @property
    def color(self):
        return self._msg_to_send[3]

    @color.setter
    def color(self, value):
        if isinstance(value, tuple) and len(value) == 3 and all(i in range(256) for i in value):
            self._msg_to_send[3] = value

    @property
    def picked_up(self):
        return self._msg_to_send[4]

    @picked_up.setter
    def picked_up(self, value):
        if value in (0, 1):
            self._msg_to_send[4] = value

    @property
    def dropped(self):
        return self._msg_to_send[5]

    @dropped.setter
    def dropped(self, value):
        if value in (0, 1):
            self._msg_to_send[5] = value
