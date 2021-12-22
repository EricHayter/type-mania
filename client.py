import socket
import time
import json
from game import percentComplete 

HEADER = 64
PORT = 6050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def setup():
    try:
        client.connect(ADDR)
        print(f"Connected to {SERVER} on port {PORT}")
    except:
        return None

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    return client.recv(2048).decode(FORMAT)

def client():
    while 1:
        time.sleep(0.016)
        score_message = f"{percentComplete(current_text, target_text)}" 
        if len(score_message) == 2 and score_message.split()[1] == "100":   
            break

        scores.update(json.loads(send(score_message)))
        
