import socket


class Client():

    def __init__(self):
        self.HEADER = 64
        self.PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = '127.0.0.1'
        self.ADDR = (self.SERVER, self.PORT)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect(self.ADDR)

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.sock.send(send_length)
        self.sock.send(message)
        print(self.sock.recv(2048).decode(self.FORMAT))

    def disconnect(self):
        self.send(self.DISCONNECT_MESSAGE)


if __name__ == "__main__":
    c = Client()
    c.connect()

    c.send("Hello World!")
    input()
    c.send("Hello Everyone!")
    input()
    c.send("Hello Eric!")
    c.disconnect()