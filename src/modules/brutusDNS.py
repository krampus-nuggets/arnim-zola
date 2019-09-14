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
import time

def killpid(signum=0, frame=0):
    print( "\r\x1b[K" )
    os.kill(os.getpid(), 9)
