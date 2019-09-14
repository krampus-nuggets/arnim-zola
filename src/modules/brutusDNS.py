#!/usr/bin/python3

from sys import argv, stdout
from os import getpid, kill
from socket import *
from threading import Thread, Lock
import subprocess
from signal import SIGINT, signal
import dns.resolver
from queue import Queue
import argparse
import gzip
import json
import time as arnimTime

def killpid(signum=0, frame=0):
    print("\r\x1b[K")
    os.kill(os.getpid(), 9)

signal(SIGINT, killpid)

class arnimThread(Thread):
    def __init__(self, threadID, name, e):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.e = q

    def run(self):
        process_data(self.name, self.q)

