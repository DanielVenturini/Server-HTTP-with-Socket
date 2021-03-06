# -*- coding:ISO-8859-1 -*0

import json
from methods.Operation import Operation

class Virtual:

    def __init__(self, get):
        self.method = get

    def start(self):            # is not a thread
        if(self.getResource() == False):
            self.method.response.response404()
            return

        self.getVirtual()

    def getResource(self):
        try:
            self.resourcePath = self.method.resourcePath

            # http://host:80/virtual/telemetria/status.json -> 'virtual/telemetria/status.json'
            if(self.resourcePath[self.resourcePath.rindex('.')+1:].__eq__('json')):
                self.virtual = self.resourcePath[1:self.resourcePath.rindex('.')]            # status.json -> 'status'
                return True
            else:
                return False

        except ValueError:      # the user can send the requeste 'status' without '.json'

            if(self.resourcePath.__contains__('feedback')):   # if it's feedback, it dosen't have the point
                self.virtual = 'feedback'
                return True

            return False        # it's not status ou feedback

    def getVirtual(self):
        try:
            if(self.virtual.__eq__('/virtual/telemetria/status')):
                self.getStatus()
            elif(self.virtual.__eq__('feedback')):
                self.saveFeedback()
            else:
                self.method.response.response404()
        except AttributeError:
            self.method.response.response404()

    def getStatus(self):
        responseClient = 'HTTP/1.1 200 OK\r\n ' + \
        'Server: Venturini/1.1\r\n' + \
        'Date: ' + self.method.operation.getCurrentDate() + '\r\n' + \
        'Set-Cookie: ' + self.method.operation.getCookies() + '\r\n' + \
        'Content-Type: application/json\r\n\r\n' + self.getJson()

        self.method.response.send(responseClient)

    def getJson(self):
        return json.dumps(
            {
                'requests' : str(self.method.reqCount),
                'connecteds' : self.method.servers,
                'uptime' : self.method.upTime,
                'currenttime' : Operation(None, None, None).getCurrentDate()
            }
        )

    def saveFeedback(self):
        bodyLines = self.method.httpBody[-1].split('&') # separe in lines
        self.saveFromBody(bodyLines)                    # separe all header and values

    def saveFromBody(self, bodyLines):

        nameFile = Operation(None, None, None).getCurrentDate()         # only get the current date to be the of file
        file = open('feedback/' + self.parseDate(nameFile), 'w+')       # create a new file

        for line in bodyLines:
            line = line.split('=')
            file.write(line[0] + ' \'' + line[1].replace('%2C', ', ').replace('+', ' ') + '\'\r\n')

        try:
            file.write('Host ' + self.method.headerFields['Host'] + '\r\n')
            file.write('Referer ' + self.method.headerFields['Referer'] + '\r\n')
            file.write('Cookie ' + self.method.cookies + '\r\n')
            file.write('User-Agent ' + self.method.headerFields['User-Agent'] + '\r\n')
        except KeyError:
            pass
        except :
            pass

        file.close()

    # transform 'Mon, 21 May 2018 23:35:17 GMT' in 'Mon21May201823:35:17GMT'
    def parseDate(self, date):
        return date.replace(' ', '').replace(',', '')