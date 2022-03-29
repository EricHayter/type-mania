import json
import socket


class Client():
    HEADER = 8
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
        # send message to server
        msg = bytes(msg, Client.FORMAT)
        msg_length = len(msg)
        send_length = str(msg_length).encode(Client.FORMAT)
        send_length += b' ' * (Client.HEADER - len(send_length))
        self.sock.send(send_length)
        self.sock.send(msg)

    def recieve(self):
        msg_length = self.sock.recv(Client.HEADER).decode(Client.FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.sock.recv(msg_length).decode(self.FORMAT)
            return msg

    def setup(self):
        # sending the actual message
        self.send(json.dumps(self.getScore()))
        msg_rcv = self.recieve()
        self.setScore(json.loads(msg_rcv))


if __name__ == "__main__":
    c = Client(5050, None, None)
    c.connect()

    c.setup()
    c.disconnect()
