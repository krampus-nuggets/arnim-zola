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

maxThreads = 500
def killpid(signum=0, frame=0):
    print("\r\x1b[K")
    os.kill(os.getpid(), 9)

signal(SIGINT, killpid)

class arnimThread(Thread):
    def __init__(self, threadID, name, q):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        process_data(self.name, self.q)

class arnimPrinter:
    def __init__(self, data):
        stdout.write("\r\x1b[K" + data.__str__())
        stdout.flush()

class Timer:
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
    writeOut("bad")
    kill(getpid(), 9)

def writeOut(state):
    logfile = open("logs/" + domain + ".log", "w")
    for item in found:
        logfile.write("%s\n" % item)
    if state == "good":
        print("\n [*] Processes complete - " + str(len(found)) + " Sub-Domains found.")
    else:
        print("\n  [*] Processes Aborted - " + str(progdone) + " Lookups Completed & " + str(len(found)) + "Sub-Domains found.")
    print(" [*] Results saved to logs/" + domain + ".log")

def processData(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            host = data.strip() + "." + domain.strip()
            try:
                answers = resolver.query(host)
                try:
                    output = gethostbyaddr(host)
                    if len(host) < 16:
                        stdout.write("\r\x1b[K")
                        stdout.flush()
                        print("\r" + str(host) + "\t\t" + str(output[0]) + " " + str(output[2]))
                        found.append(str(host) + "\t\t" + str(output[0]) + " " + str(output[2]))
                    else:
                        stdout.write("\r\x1b[K")
                        stdout.flush()
                        print("\r" + str(host) + "\t" + str(output[0]) + " " + str(output[2]))
                except:
                    stdout.write("\r\x1b[K")
                    stdout.flush()
                    print("\r" + str(host))
                    found.append(str(host))
            except:
                pass
        else:
            queueLock.release()

zolaParser = argparse.ArgumentParser(prog="brutusDNS", usage="brutusDNS [options]")
zolaParser.add_argument("-u", "--url", type=str, help="eg. --url google.com")
zolaParser.add_argument("-w", "--wordlist", type=str, help="eg. --wordlist /root/BitchBeGone.txt")
zolaParser.add_argument("-t", "--threads", type=int, help="eg. --threads 10 | Amount of threads to use -_-")
zolaParser.add_argument("-a", "--att", type=str, help="Add additional attributes")
args = zolaParser.parse_args()

if len(argv) == 1:
    zolaParser.print_help()
    exit()

if args.threads:
    maxThreads = args.threads

serversDNS = ["8.8.8.8", "8.8.4.4", "4.2.2.1", "4.2.2.2", "4.2.2.3", "4.2.2.4", "4.2.2.5", "4.2.2.6", "4.2.35.8",
              "4.2.49.4", "4.2.49.3", "4.2.49.2", "209.244.0.3", "209.244.0.4", "208.67.222.222", "208.67.220.220",
              "192.121.86.114", "192.121.121.14", "216.111.65.217", "192.76.85.133", "151.202.0.85"]

signal(SIGINT, killpid)


