#!usr/bin/python3/

from alg_utils import *
import sys
import os
import datetime 

def bruteforce(G, coloring, num_nodes):
  neigh_diff = getNeighDiff(G, coloring)
  pairs = getPairs(neigh_diff)
  nodes = list(G.nodes)
  coverageFull = getCoverage(neigh_diff, len(nodes))
  combinations = itertools.dropwhile(lambda x: checkConnectionsFaster(x, pairs, coverageFull)!=0, itertools.chain.from_iterable(itertools.combinations(nodes, r) for r in range(1, len(nodes)+1)))
  return list(combinations)[0]


def main():
  if len(sys.argv) != 6:
    error("Invalid number of arguments")
  INPUT_DIR = sys.argv[1]
  OUTPUT_DIR = sys.argv[2]
  try:
    NUM_INSTANCES = int(sys.argv[3])
    NUM_NODES = int(sys.argv[4])
    PROB_EDGES = float(sys.argv[5])
  except ValueError:
    error("Not a number number")


  if not os.path.exists(INPUT_DIR):
    error("Filepath not valid " + INPUT_DIR)

  if not os.path.exists(OUTPUT_DIR):
    error("Filepath not valid " + OUTPUT_DIR)

  filesWithSpecs = [f for f in os.listdir(INPUT_DIR) if  f.find(f"graph_{NUM_NODES:03}_{int(PROB_EDGES*100):03}")!=-1]
  filesWithSpecs.sort()
  iFiles = [INPUT_DIR+f for f in filesWithSpecs]
  oFiles = [OUTPUT_DIR+f.replace("graph", "bruteforce") for f in filesWithSpecs]
 
  instances = [readFromFile(f) for f in iFiles]
  instances = [(i[0], getSeparateColors(i[1])) for i in instances]
  
  times = []
  solutions = []

  for i in range(NUM_INSTANCES):
      start_time = datetime.datetime.now()
      solution = bruteforce(instances[i][0], instances[i][1], NUM_NODES)
      end_time = datetime.datetime.now()
      times.append((end_time-start_time).total_seconds())
      solutions.append(solution)
      writeSolutionInFile(oFiles[i], times[i], solutions[i])

  writeInCsv(f"{OUTPUT_DIR:s}BRUTEFORCE_{NUM_NODES:03}_{int(PROB_EDGES*100):03}.csv", times, solutions, NUM_INSTANCES)

if __name__=="__main__":
  main()
