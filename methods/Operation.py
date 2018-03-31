# -*- coding:ISO-8859-1 -*-
from datetime import datetime   # datetime.strptime()
from os import path             # os.path.getmtime()
import time                     # time.localtime()
import os                       # os.listdir()

class Operation:

    def __init__(self, cookies):
        self.cookies = cookies

    def currentFile(self, dateClient, dateServer):
        if(dateClient >= dateServer):
            return "CLIENT"
        else:
            return "SERVER"

    def lastModified(self, resourcePath, getDate):      # get the Object date or string with the date of last modified
        date = ['Mon, ', 'Tue, ', 'Wed, ', 'Thu, ', 'Fri, ', 'Sat, ', 'Sun, ']
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        t = time.localtime(path.getmtime(resourcePath))             # get the time of file on server
        strDate = date[t.tm_wday]
        date = datetime.strptime(strDate + str(t.tm_mday) + " " + str(t.tm_mon) + " " + str(t.tm_year) + " " + str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec) + " " + " GMT", "%a, %d %m %Y %H:%M:%S %Z")
        strDate += str(t.tm_mday) + " " + month[t.tm_mon-1] + " " + str(t.tm_year) + " " + str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec) + " " + " GMT"

        if(getDate):
            return date
        else:
            return strDate

    def getCookies(self):
        if(self.cookies == {}):
            return "count=0"
        else:
            return "count=" + str(int(self.cookies["count"])+1)

    def getResourcePathName(self, resourcePath):
        # If '/', return index.html. Some browers request from the 'favicon.ico' of the page. If none, concat the '.'
        if(resourcePath == "/index.html"): resourcePath = "./"
        elif(resourcePath == "/favicon.ico"): resourcePath = "./photos/favicon.ico"
        else: resourcePath = "." + resourcePath

        return resourcePath

    def getCurrentDate(self):
        weekday = ['Mon, ', 'Tue, ', 'Wed, ', 'Thu, ', 'Fri, ', 'Sat, ', 'Sun, ']
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        propertyTime = time.localtime()
        strDate = ""            # Wed, 21 Oct 2015 07:28:00 GMT

        strDate += weekday[propertyTime.tm_wday]
        strDate += (str(propertyTime.tm_mday) + ' ')
        strDate += (month[propertyTime.tm_mon-1] + ' ')
        strDate += (str(propertyTime.tm_year) + ' ')
        strDate += (str(propertyTime.tm_hour) + ':')
        strDate += (str(propertyTime.tm_min) + ':')
        strDate += (str(propertyTime.tm_sec) + ' GMT')

        return strDate

    def getIndex(self, resourcePath):

        indexhtml = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">' +\
                    '<html>' +\
                    '<head>' +\
                    '<title>Index of ' + resourcePath[1:] + '</title>' +\
                    '</head>' +\
                    '<body style="background-color: AliceBlue;">' +\
                    '<h1>List of files in ' + resourcePath[1:] + '</h1><hr>' +\
                    '<table><tr><td><img src="./photos/index.png"></td><td><h2>File</h2></td><td><h2>Size</h2></td></tr><hr>'

        files = os.listdir(resourcePath)
        for i in range(0, len(files)):
            files[i] = (resourcePath + '/' + files[i])      # complete the path: 'background.png' => './photos/background.png'

            if(path.isfile(files[i])):
                icon = './photos/file-icon.png'
            else:
                icon = './photos/folder-icon.png'

            indexhtml += ('<tr><td><img src='+icon+'></td><td><a href='+files[i][2:]+'>'+files[i][2:]+'</a></td><td>'+str(path.getsize(files[i]))+' B</td></tr>') # new register in the table

        indexhtml += '</table><hr><address>Venturini/1.1<address></body></html>'

        return indexhtml