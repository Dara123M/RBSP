from alg_utils import *
from utils import *
import datetime
import sys
import os

OUTPUT_DIR_FIT = 'greedy_instances_fit/'

def greedy(G, coloring, num_nodes, filename):
    reds, blues = coloring
    neigh_diff = getNeighDiff(G, coloring)
    fullcoverage = getCoverage(neigh_diff, num_nodes)
    pairs = getPairs(neigh_diff)

    coverage = getCoverage(neigh_diff, num_nodes)
    pairs_cov_len = sorted([(len(coverage[v]), v) for v in coverage.keys()], key=lambda x: (x[0],-x[1]), reverse=True)
    s = set()
    
    iter = 1
    while checkConnectionsFaster(s, pairs, fullcoverage)!=0:
        max_coverage_vertex = pairs_cov_len[0]
        
        s.add(max_coverage_vertex[1])
        writeFitnessInCsv(filename, iter, s, checkConnectionsFaster(s, pairs, fullcoverage))
        for pair in coverage[max_coverage_vertex[1]]:
            if pair in neigh_diff.keys():
               del neigh_diff[pair]
        
        coverage = getCoverage(neigh_diff, num_nodes)
        pairs_cov_len = sorted([(len(coverage[v]), v) for v in coverage.keys()],  key=lambda x: (x[0],-x[1]), reverse=True)
        iter +=1 
    return sorted(s), checkConnectionsFaster(s, pairs, fullcoverage) 


def main():
    random.seed(42)
    argv = sys.argv[1].split(' ')
    
    if len(argv) != 4:
       error("Invalid number of arguments")
    INPUT_DIR = argv[0]
    OUTPUT_DIR = argv[1]
    try:
        NUM_INSTANCES = int(argv[2])
        NUM_NODES = [10, 20, 30, 50, 100, 200, 250]#int(sys.argv[4])
        PROB_EDGES = float(argv[3])
    except ValueError:
        error("Not a number number")


    if not os.path.exists(INPUT_DIR):
      error("Filepath not valid " + INPUT_DIR)

    if not os.path.exists(OUTPUT_DIR):
      error("Filepath not valid " + OUTPUT_DIR)

    for n in NUM_NODES:
        filesWithSpecs = [f for f in os.listdir(INPUT_DIR) if  f.find(f"graph_{n:03}_{int(PROB_EDGES*100):03}")!=-1]
        filesWithSpecs.sort()
        iFiles = [INPUT_DIR+f for f in filesWithSpecs]
        oFiles = [OUTPUT_DIR+f.replace("graph", "greedy") for f in filesWithSpecs]
        fitFiles = [OUTPUT_DIR_FIT+f.replace("graph", "greedy_instances_fit") for f in filesWithSpecs]
        fitFiles = [f.replace("txt", "csv") for f in fitFiles]

        instances = [readFromFile(f) for f in iFiles]
        instances = [(i[0], getSeparateColors(i[1])) for i in instances]

        times = []
        solutions = []
        costs = []
        for i in range(NUM_INSTANCES):
            start_time = datetime.datetime.now()
            solution, cost = greedy(instances[i][0], instances[i][1], n, fitFiles[i])
            end_time = datetime.datetime.now()
            times.append((end_time-start_time).total_seconds())
            solutions.append(solution)
            costs.append(cost)
            writeSolutionInFile(oFiles[i], times[i], solutions[i], cost)

        writeInCsv(f"{OUTPUT_DIR:s}GREEDY_{n:03}_{int(PROB_EDGES*100):03}.csv", times, solutions, NUM_INSTANCES)

if __name__=="__main__":
  main()