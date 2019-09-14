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

class arnimPrinter:
    def __init__(self, data):
        self.start = arnimTime.time()

    def __exit__( self, *args ):
        sec = int(arnimTime.strftime('%S', arnimTime.gmtime(taken)))
        min = int(arnimTime.strftime('%M', arnimTime.gmtime(taken)))
        hour = int(arnimTime.strftime('%H', arnimTime.gmtime(taken)))
        if min > 0:
            if hour > 0:
                print(" [*] Time Elapsed - " + str(hour) + " hours, " + str(min) + " minutes and " + str(sec) + " seconds at " + str(round(len(subdomains) / taken, 2)) + " lookups per second.")
            else:
                print(" [*] Time Elapsed - " + str(min) + " minutes and " + str(sec) + " seconds at " + str(round(len(subdomains) / taken, 2)) + " lookups per second.")
        else:
            print(" [*] Time Elapsed - " + str(sec) + " seconds at " + str(round(len(subdomains) / taken, 2)) + " lookups per second.")

def killpid():
    writeout("bad")
    kill(getpid(), 9)

