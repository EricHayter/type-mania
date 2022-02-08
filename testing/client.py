import socket
import random
import time
import json

HOST = '127.0.0.1'
PORT = 4321

score = {}
scores = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 4321))

print(f'connected to {HOST} on port {PORT}')

for x in range(1, 10):
    print(repr(s.recv(1024)))