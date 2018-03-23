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

    def readFile(self, data):
        msgHTTP = data.split()
        self.method = msgHTTP[0]

        if(msgHTTP[1] == "/"): self.path = "./index.html"
        elif(msgHTTP[1] == "/favicon.ico"): self.path = "./photos/favicon.ico"
        else: self.path = "." + msgHTTP[1]

        self.version = msgHTTP[2]

        self.header = {}
        for i in range(3, len(msgHTTP), 2):
            self.header[msgHTTP[i]] = msgHTTP[i+1]

    def methods(self, data):
        self.readFile(data)

        if(self.method == 'GET'):
            print("Return the file " + self.path)
            try:
                return 'HTTP/1.1 200 OK\r\n\r\n' + open(self.path, "r").read()
            except IOError:
                print("File not found")
                return "HTTP/1.1 404 Not Found\r\n"
        else:
            return "HTTP/1.1 503 Service Unavailable\r\n"

    def attending(self, conn, addr):
        print("---------Connection address:", addr, "---------")
        data = conn.recv(self.BUFFER_SIZE)
        conn.sendall(self.methods(data))    # echo
        conn.close()

    def running(self):
        print("Running server in " + self.TCP_IP + ":" + str(self.TCP_PORT))
        print("---------Waiting for connection---------")

        while True:     # ever on
            conn, addr = self.s.accept()
            threading.Thread(target = self.attending, args = (conn, addr)).start()
            continue

# ----------- END OF CLASS ----------- #

Server('192.168.0.105', 5005)