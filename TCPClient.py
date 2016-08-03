# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 20:30:51 2016

@author: Tracy Marshall
"""

import socket
#import rsa

TCP_IP = '192.168.0.113'
HOST = ''
TCP_PORT = 50021
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

print('Creating socket...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Socket connecting...')
s.connect((TCP_IP, TCP_PORT))

print('Socket sent: ' + MESSAGE)
s.send(MESSAGE.encode())


data = s.recv(BUFFER_SIZE)

print('Received: ' + str(data))
s.close()

#print("Sent data:", data)