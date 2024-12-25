#!/usr/bin/python3
DIR_PATH = "graphs/"
from utils import *
import sys
import os

if len(sys.argv) < 3:
    error("Two arguments are needed, directory and number of instances")

if not os.path.exists(sys.argv[1]):
    error("Invalid Path: directory does not exist")

DIR_PATH = sys.argv[1]

try:
    NUM_INSTANCE = abs(int(sys.argv[2]))
except ValueError:
    error("Expected number for instances")

if len(sys.argv[2:])>1:
    try:
        NUM_NODES = [abs(int(sys.argv[3]))]
    except ValueError:
        error("Excepted number of nodes and probability")


if len(sys.argv[3:])>1:
    try:
        PROB_EDGES = [abs(int(sys.argv[4]))]
    except ValueError:
        error("Excepted number of nodes and probability")


for n in NUM_NODES:
    for p in PROB_EDGES:
        instances = generateInstances(n, p, NUM_INSTANCE)
        colors = [colorGraph(g) for g in instances]
        for i in range(NUM_INSTANCE):
            filename = f"{DIR_PATH:s}graph_{n:03}_{int(p*100):03}_{i+1:02}.txt"
            writeInFile(filename, instances[i], colors[i])
    
