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
