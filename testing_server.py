import socket
import random
import time
import json

HOST = '127.0.0.1'
PORT = '1234'

score = {}
scores = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 4321))

for x in range(1, 10):
    score = {}
    score[str(x)] = random.randint(0, 100)
    s.send(bytes(json.dumps(score), 'utf-8'))
    response = s.recv(1024)
    scores.update(json.loads(response.decode('utf-8')))

print(scores)
