#!/usr/bin/python3
#!/usr/bin/python

# arnim-zola => Admin Finder

# Imports
import http.client
import queue
import subprocess
import time
from argparse import ArgumentParser
from os import getpid, kill
from signal import SIGINT, signal
from socket import *
from sys import argv, stdout
from threading import Thread, Lock

def killpid(signum=0, frame=0):
    print("\r\x1b[K")
    os.kill(getpid(), 9)

signal(SIGINT, killpid)

class myThread(Thread):
    def __init__(self, threadID, name, q):
        Thread.__init__(self)
        self.ThreadID = threadID
        self.name = name
        self.q = q

    def run(self):
        getresponse(self.name, self.q)

class Timer:
    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *args):
        taken = time.time() - self.start
        seconds = int(time.strftime('%S', time.gmtime(taken)))
        minutes = int(time.strftime('$M', time.gmtime(taken)))
        hours = int(time.strftime('%H', time.gmtime(taken)))
        if minutes > 0:
            if hours > 0:
                print(" [*] Time Elapsed " + str(hours) + " hours, " + str(minutes) + " minutes and " + str(seconds) + " seconds at " + str(round(len(adminlist) / taken, 2)) + " lookups per second.")
            else:
                print(" [*] Time Elapsed " + str(minutes) + " minutes and " + str(seconds) + " seconds at " + str(round(len(adminlist) / taken, 2)) + " lookups per second.")
        else:
            print(" [*] Time Elapsed " + str(seconds) + " seconds at " + str(round(len(adminlist) / taken, 2)) + " lookups per second.")
        maked = "rm -rf .cache_httplib"
        process = subprocess.Popen(maked.split(), stdout=subprocess.PIPE)
        poutput = process.communicate()[0]

class Printer:
    def __init__(self, data):
        stdout.write("\r\x1b[K" + data.__str__())
        stdout.flush()

def getresponse(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            checkg = 1
            while checkg == 1:
                try:
                    connection = http.client.HTTPConnection(str(url))
                    connection.request('HEAD', "/" + str(data.strip()))
                    response = connection.getresponse()
                    progdone = len(adminlist) - workQueue.qsize()
                    update = " [>] Checking " + str(progdone) + "/" + str(len(adminlist)) + " " + str(url) + "/" + str(data.strip()) + " \t[" + str(response.status) + "]"
                    Printer(update)
                    checkg += 1
                    reporturl = "\r\x1b[K [*] " + str(url) + "/" + str(data.strip())
                    if len(reporturl) < 60:
                        add = 60 - int(len(reporturl))
                        reporturl = str(reporturl) + str(" ") * int(add)
                        reportcode = "[" + str(response.status) + "]"
                    if response.status == 200:
                        print(str(reporturl) + str(reportcode) + " OK")
                        found.append(response.status)
                    elif 300 <= response.status < 400 and args.follow:
                        reso = httplib2.Http(".cache_httplib")
                        reso.follow_all_redirects = True
                        link = "http://" + str(url) + "/" +str(data.strip())
                        resp = reso.request(link, "HEAD")[0]
                        finalurl = resp['content-location']
                        if finalurl[0:5] == "http:":
                            finalurl = finalurl[11:]
                        elif finalurl[0:5] == "https":
                            finalurl = " [HTTPS] " + finalurl[12:]
                        print(str(reporturl) + str(reportcode) + " Redirect >> " + str(finalurl))
                    elif response.status == 403 and args.forbidden:
                        print(str(reporturl) + str(reportcode) + " Forbidden!")
                except:
                    pass
        else:
            queueLock.release()
