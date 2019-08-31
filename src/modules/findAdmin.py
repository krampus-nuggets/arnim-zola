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
