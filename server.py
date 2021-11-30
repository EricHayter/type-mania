import socket
import threading
import json

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

playerCompletions = {}


def handle_client(conn, addr):
    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT).split()

            if msg[0] == DISCONNECT_MESSAGE:
                break

            id = int(msg[0])
            percentFinished = msg[1]
            playerCompletions[id] = percentFinished

            conn.send(json.dumps(playerCompletions).encode(FORMAT))

    conn.close()


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
