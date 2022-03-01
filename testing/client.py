import json
import socket


class Client():
    HEADER = 64
    SERVER = '127.0.0.1'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    FORMAT = 'utf-8'

    def __init__(self, port, getScoreFunction, setScoreFunction):
        self.PORT = port
        self.ADDR = (Client.SERVER, self.PORT)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.getScore = getScoreFunction
        self.setScore = setScoreFunction

    def connect(self):
        self.sock.connect(self.ADDR)

    def disconnect(self):
        self.send(Client.DISCONNECT_MESSAGE)

    def send(self, msg):
        message = msg.encode(Client.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(Client.FORMAT)
        send_length += b' ' * (Client.HEADER - len(send_length))
        self.sock.send(send_length)
        self.sock.send(message)
        print(self.sock.recv(2048).decode(Client.FORMAT))

    def recieve(self):
        msg = self.sock.recv(1024)
        print(f"The message is {msg}")
        return msg

    def setup(self):
        self.send(json.dumps(self.getScore()))
        msg_rcv = self.recieve()
        self.setScore(json.dumps(msg_rcv))
        return msg_rcv


if __name__ == "__main__":
    c = Client(50, None, None)
    c.connect()

    c.send("Hello World!")
    input()
    c.send("Hello Everyone!")
    input()
    c.send("Hello Eric!")
    c.disconnect()