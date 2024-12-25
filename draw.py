#!/usr/bin/python3

from utils import *
import os
from alg_utils import *
INPUT_DIR = "graphs/"
NUM_NODES = 6
PROB_EDGES = 0.2
OUTPUT_DIR = "drawings/"
NUM_INSTANCES = 10

filesWithSpecs = [f for f in os.listdir(INPUT_DIR) if  f.find(f"graph_{NUM_NODES:03}_{int(PROB_EDGES*100):03}")!=-1]
filesWithSpecs.sort()
print(filesWithSpecs)
iFiles = [INPUT_DIR+f for f in filesWithSpecs]
oFiles = [OUTPUT_DIR+f.replace("graph", "drawing") for f in filesWithSpecs]

instances = [readFromFile(f) for f in iFiles]
instances = [(i[0], getSeparateColors(i[1])) for i in instances]

for i in range(NUM_INSTANCES):
    drawColoredGraph(instances[i][0], instances[i][1], oFiles[i]) 
