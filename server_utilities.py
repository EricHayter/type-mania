import types
import socket
import selectors
import time
import json

player_scores = {}
sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print('accepted connection from ', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print(repr(recv_data))
            player_scores.update(json.loads(recv_data))
            data.outb += bytes(json.dumps(player_scores),'utf-8')

        else:
            print('closing connection to ', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

def client(player_scores, my_score, sock):
    while True:
        # sending local player's score
        sock.send(bytes(json.dumps(my_score),'utf-8'))
        server_response = sock.recv(1024)
        # server responds with everyone's score in JSON format
        try:
            player_scores.update(json.loads(server_response))
        except:
            pass
        time.sleep(0.1)

def server():
    try: 
        HOST = '127.0.0.1'
        PORT = 4321

        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((HOST, PORT))
        lsock.listen()
        print('listening on ', (HOST, PORT))
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)

        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except Exception as e:
        print(e)
        lsock.close()

if __name__ == "__main__":
    server()
