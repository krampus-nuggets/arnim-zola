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
    def __init__(self, threadID, name, q):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        processData(self.name, self.q)

class arnimPrinter:
    def __init__(self, data):
        stdout.write("\r\x1b[K" + data.__str__())
        stdout.flush()

class Timer:
    def __enter__(self):
        self.start = arnimTime.time()

    def __exit__(self, *args):
        sec = int(arnimTime.strftime("%S", arnimTime.gmtime(taken)))
        min = int(arnimTime.strftime("%M", arnimTime.gmtime(taken)))
        hour = int(arnimTime.strftime("%H", arnimTime.gmtime(taken)))
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
        print("\n  [*] Processes Aborted - " + str(progComplete) + " Lookups Completed & " + str(len(found)) + "Sub-Domains found.")
    print(" [*] Results saved to logs/" + domain + ".log")

def processData(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            host = data.strip() + "." + domain.strip()
            try:
                answers = resolverDNS.query(host)
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
                        found.append(str(host) + "\t\t" + str(output[0]) + " " + str(output[2]))
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

maxThreads = 500

if args.threads:
    maxThreads = args.threads

serversDNS = ["8.8.8.8", "8.8.4.4", "4.2.2.1", "4.2.2.2", "4.2.2.3", "4.2.2.4", "4.2.2.5", "4.2.2.6", "4.2.35.8",
              "4.2.49.4", "4.2.49.3", "4.2.49.2", "209.244.0.3", "209.244.0.4", "208.67.222.222", "208.67.220.220",
              "192.121.86.114", "192.121.121.14", "216.111.65.217", "192.76.85.133", "151.202.0.85"]

signal(SIGINT, killpid)

domain = args.url
logDIR = "mkdir -p logs"
process = subprocess.Popen(logDIR.split(), stdout=subprocess.PIPE)
procOut = process.communicate()[0]
subdomains = [line.strip() for line in open(args.wordlist, "r")]
if args.att:
    with gzip.GzipFile(open("resources/DNSCached.txt.gz"), "r") as CacheClose:
        bytesJSON = CacheClose.read()
        stringJSON = bytesJSON.decode("utf-8")
        data = json.loads(stringJSON)
        serversDNS = data

resolverDNS = dns.resolver.Resolver()
resolverDNS.nameservers = serversDNS
queueLock = Lock()
workQueue = Queue(len(subdomains))
found = []
threads = []
exitFlag = 0
threadID = 1

print("[*] Starten von " + str(maxThreads) + " zu verarbeitenden Threads und " + str(len(subdomains)) + " Unterdomänen.\n")

queueLock.acquire()

for work in subdomains:
    workQueue.put(work)

queueLock.release()

while threadID <= maxThreads:
    tName = str("Thread-") + str(threadID)
    thread = arnimThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

countStart = arnimTime.time()
arnimStart = arnimTime.time()

with Timer():
    while not workQueue.empty():
        countProg = 0.3
        progress = arnimTime.time() - arnimStart
        if progress >= countProg:
            progComplete = len(subdomains) - workQueue.qsize()
            token = arnimTime.time() - countStart
            rate = rount(progComplete / token, 2)
            percent = round(float(100.00) / len(subdomains) * progComplete, 2)
            eta = round(token / percent * 100 - token, 2)
            outputPrint = " [*] " + str(percent) + "% Complete, " + str(progComplete) + "/" + str(len(subdomains)) + " lookups at " + str(rate) + " lookups/second. ETA: " + str(arnimTime.strftime("%H:%M:%S", arnimTime.gmtime(eta)))
            arnimPrinter(outputPrint)
            startProg = arnimTime.time()
        else:
            pass

    taken = arnimTime.time() - countStart
    stdout.write("\r\x1b[K")
    stdout.flush()

    for e in threads:
        e.join()

    writeOut("gut. Alle möglichen DNS-Server aufgelöst.")
