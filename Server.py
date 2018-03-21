# -*- coding:ISO-8859-1 -*-

import socket
import threading

class Server:

    def __init__(self, TCP_IP, TCP_PORT):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = 512          # Normally 1024, but we want fast response

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((TCP_IP, TCP_PORT))
        self.s.listen(5)

        self.running()

    def attending(self, conn, addr):
        response = 'HTTP/1.1 200 OK\r\nHello Brasil!'
        print("---------Connection address:", addr, "---------")
        while 1:
            data = conn.recv(self.BUFFER_SIZE)
            if not data:
                break

            print("received data:", data)
            conn.sendall(response)  # echo

        conn.close()

    def running(self):
        print("\n\nRunning server in " + self.TCP_IP + ":" + str(self.TCP_PORT))
        print("---------Waiting for connection---------")

        while True:     # ever on
            conn, addr = self.s.accept()
            threading.Thread(target = self.attending, args = (conn, addr)).start()
            continue

# ----------- END OF CLASS ----------- #




Server('127.0.0.1', 5005)
print("Voltou")