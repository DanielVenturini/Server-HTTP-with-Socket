# -*- coding:ISO-8859-1 -*-

from methods import Operation
from Worker import Worker
from Grid import Grid
import network
import socket

class Server:

    def __init__(self, PORT_HTTP, PORT_UNICAST):
        self.IP, BROADCAST = network.getIP_BC() # get the IP and BROADCAST address of this machine based in the 'ifconfig'
        # IP, BROADCAST = '172.16.1.13', '172.16.1.63'
        self.PORT_HTTP = PORT_HTTP
        self.BUFFER_SIZE = 2048                 # Normally 1024, but we want fast response
        self.servers = {}

        # only get the upTime and count of request. Both for the path virtual 'status.json'
        self.upTime = Operation.Operation(None, None, None).getCurrentDate()
        self.reqCount = 0

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((self.IP, PORT_HTTP))
        except socket.error:
            self.s.bind((self.IP, 0))
            self.PORT_HTTP = self.s.getsockname()[1]

        grid = Grid(self.IP, PORT_HTTP, PORT_UNICAST, BROADCAST, self.servers)  # create the grid class
        grid.start()                                                            # execute thread

        self.s.listen(5)
        self.running()

    def running(self):
        print("Wait for new connections on http://" + self.IP + ":" + str(self.PORT_HTTP))

        while True:     # ever on
            self.reqCount += 1
            conn, addr = self.s.accept()
            thread = Worker(conn, addr, conn.recv(self.BUFFER_SIZE), self.servers, self.reqCount, self.upTime, self.IP, self.PORT_HTTP)  # create thread
            thread.start()                                                                                      # execute thread
            continue

# ----------- END OF CLASS ----------- #

Server(5555, 5554)
