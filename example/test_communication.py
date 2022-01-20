#!/usr/bin/env python3

"""
License: You are free to use any part of code in this project as long as you mention original authors of this program:
Alpha Team composed of: Nirmalraj JEYANATHAN Joseph - SERFATY Milan - YE Hang - ZHANG Yujia

Supervised by Aurore (aurore.isep@gmail.com) and Hugo (myrobotswillconquertheworld@gmail.com)
IE.3510 (System Modeling) - ISEP 2022
"""

import time
import socket

s = socket.socket()
s.connect(('172.20.10.3', 5204))
try:
    while True:
        # print("From Server: ", s.recv(1024))  #This gets printed after sometime
        # print("From Server: ", s.recvmsg(1024))  #This gets printed after sometime
        # s.send(input("Client please type: ").encode())
        s.send("&ZE\nABC\n".encode())
        # s.send("ABC\n".encode())
        time.sleep(1)
except:
    s.close()
