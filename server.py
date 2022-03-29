import json
import socket
import threading
import time


class Server():
    # class variablees
    HEADER = 8
    SERVER = '127.0.0.1'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    START_MESSAGE = "!START"
    FORMAT = 'utf-8'

    # instance variables
    def __init__(self):
        self.PORT = 5050
        self.ADDR = (Server.SERVER, self.PORT)
        self.gameRunning = False
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.scores = {}

    def bind(self):
        self.server.bind(self.ADDR)

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        msg_length = conn.recv(Server.HEADER).decode(Server.FORMAT)
        msg = conn.recv(int(msg_length)).decode(Server.FORMAT)

        print(len(msg_length))

        try:
            self.scores.update(json.loads(msg))
        except:
            print(f"[{addr}] Disconnected")
            return

        while len(self.scores) < 4:
            #
            self.send(json.dumps(self.scores))
            if (self.gameRunning):
                break
            time.sleep(0.5)

        self.send(conn, Server.START_MESSAGE)

        while True:
            msg_length = conn.recv(Server.HEADER).decode(Server.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.FORMAT)
                if msg == self.DISCONNECT_MESSAGE:
                    print(f"[{addr}] Disconnected")
                    break

                print(repr(msg))
                conn.send("Msg received".encode(self.FORMAT))

        conn.close()

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {Server.SERVER}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client,
                                      args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count()}")

    def startGame(self):
        self.gameRunning = True

    def send(self, conn, msg):
        msg_length = len(msg.encode(Server.FORMAT))
        send_length = str(msg_length).encode(Server.FORMAT)
        send_length += b' ' * (Server.HEADER - len(send_length))
        conn.send(send_length)
        conn.send(msg.encode(self.FORMAT))


if __name__ == "__main__":
    print("[STARTING] server is starting...")
    s = Server()
    s.bind()
    s.start()

    threading.Thread(target=s.start).start()

    s.startGame()
