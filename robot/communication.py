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

        # Data to send
        self.reset_msg()

        self._is_connected = False
        self._connect()

    def _connect(self):
        self.socket.connect((self.host, self.port))
        self._is_connected = True

        # Start sending messages to server
        self.__send_thread = Thread(target=self._send_msg)
        self.__send_thread.setDaemon(True)
        self.__send_thread.start()

    def disconnect(self):
        self._is_connected = False

    def _send_msg(self):
        previous_msg = 0
        while self._is_connected:
            try:
                if self._msg_to_send != previous_msg:
                    # self.socket.send("&ZE\nABC\n".encode())
                    self.socket.send(self.parse_msg().encode())
                    previous_msg = self._msg_to_send.copy()
            except Exception:
                print("Error occurred while sending message")
            time.sleep(0.01)
        self.socket.close()

    def parse_msg(self):
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
        # TODO: choose a good init value for color

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
