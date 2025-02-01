
from utils import *
from alg_utils import *
from copy import deepcopy
import random
import datetime
import sys
import os
SOLUTION_PROB = 0.1
OUTPUT_DIR_FIT = 'vns_instances/'
ITER_MAX = 500
K_MAX = 2

def initializeGreedy(neigh_diff, pairs, coverage, num_nodes):
    solution = set()
    nd = neigh_diff.copy()
    cover = coverage.copy()
    pairs_cov_len = sorted([(len(cover[v]), v) for v in cover], key=lambda x: (x[0], -x[1]), reverse=True)
    while checkConnectionsFaster(solution, pairs, coverage)!=0:
        v = pairs_cov_len[0]
        solution.add(v[1])
        for p in cover[v[1]]:
           if p in nd.keys():
              del nd[p]
        cover = getCoverage(nd, num_nodes)
        pairs_cov_len = sorted([(len(cover[v]), v) for v in cover], key=lambda x: (x[0], -x[1]), reverse=True)
    
   
    return solution
    

def initializeSolution(num_nodes, prob):
    solution = [1 if random.uniform(0, 1) < prob else 0 for _ in range(num_nodes)]
    return set(getNodesFromSolution(solution))

def shakeSolution(solution, num_nodes, k=1):
  
    nodesInSolution = [i for i in solution]
    nodesNotInSolution = [i for i in range(num_nodes) if i not in nodesInSolution]
    
    random.shuffle(nodesInSolution)
    random.shuffle(nodesNotInSolution)

    k = min(k, len(nodesInSolution))  
    new_solution_nodes = nodesInSolution[:-k] + nodesNotInSolution[:k]
    
    return set(new_solution_nodes)

def swapNodeInSolution(nodesInSolution, node):
    nodesCopy = nodesInSolution.copy()  
    if node in nodesCopy:
        nodesCopy.remove(node)
    else:
        nodesCopy.add(node)
    return nodesCopy


def localSearchFirstImproved(solution, pairs, coverageFull, num_nodes):

    improved = True
    new_solution_nodes = solution.copy()
    new_solution_num_nodes = len(new_solution_nodes)
    new_solution_cost = checkConnectionsFaster(new_solution_nodes, pairs, coverageFull)
    
    all_nodes = list(range(num_nodes))
    
    while improved:
        improved = False
        random.shuffle(all_nodes)
        
        for node in all_nodes:
            current_solution_nodes = swapNodeInSolution(new_solution_nodes, node)
            current_solution_cost = checkConnectionsFaster(current_solution_nodes, pairs, coverageFull)
            if (current_solution_cost, len(current_solution_nodes)) < (new_solution_cost, new_solution_num_nodes):
                improved = True
                new_solution_nodes = current_solution_nodes.copy()
                new_solution_num_nodes = len(current_solution_nodes)
                new_solution_cost = current_solution_cost
                break
    
    return new_solution_nodes, new_solution_cost


def variableNeighborhoodSearch(G, coloring, num_nodes, iter_max, k_max, fitFile):
    neigh_diff = getNeighDiff(G, coloring)
    pairs = getPairs(neigh_diff)
    coverageFull = getCoverage(neigh_diff, num_nodes)
    solution = initializeGreedy(neigh_diff, pairs, coverageFull, num_nodes)
    cost = checkConnectionsFaster(solution, pairs, coverageFull)

    iter = 1
    k = 1
    while iter < iter_max:
        if iter % 10 == 1:
            writeFitnessInCsv(fitFile, iter, solution, cost)
            print(f"iteration: {iter}\n solution:\n {solution}\n cost: {cost}")
        iter += 1

        new_solution = shakeSolution(solution, num_nodes, k)

        solutionLocalSearch, solutionLocalSearchCost = localSearchFirstImproved(new_solution, pairs, coverageFull, num_nodes)

        if (cost, len(solution)) > (solutionLocalSearchCost, len(solutionLocalSearch)) or   ((cost, len(solution)) == (solutionLocalSearchCost, len(solutionLocalSearch)) and random.uniform(0, 1) < 0.5):
            solution = solutionLocalSearch.copy()
            cost = solutionLocalSearchCost
            k = 1
        else:
            k+=1
            if k>k_max:
                k = 1


    return sorted(solution), cost
     


def main():
  random.seed(42)
  argv = sys.argv[1].split(' ')
  if len(argv) != 4:
    error("Invalid number of arguments")
  INPUT_DIR = argv[0]
  OUTPUT_DIR = argv[1]
  try:
    NUM_INSTANCES = int(argv[2])
    NUM_NODES = [250, 10, 20, 30]
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
    oFiles = [OUTPUT_DIR+f.replace("graph", "vns") for f in filesWithSpecs]
    fitFiles = [OUTPUT_DIR_FIT+f.replace("graph", "vns_fitnes") for f in filesWithSpecs]
    fitFiles = [f.replace("txt", "csv") for f in fitFiles]
    instances = [readFromFile(f) for f in iFiles]
    instances = [(i[0], getSeparateColors(i[1])) for i in instances]
  
    times = []
    solutions = []
    costs = []
    if NUM_INSTANCES > len(instances):
      NUM_INSTANCES = len(instances)
      print(f"Not enough instances! Number of instances reduced to {len(instances)}")

    for i in range(NUM_INSTANCES):
      start_time = datetime.datetime.now()

      solution, cost = variableNeighborhoodSearch(instances[i][0], instances[i][1], n, ITER_MAX, K_MAX, fitFiles[i])
      end_time = datetime.datetime.now()
      times.append((end_time-start_time).total_seconds())
      solutions.append(solution)
      costs.append(cost)
      writeSolutionInFile(oFiles[i], times[i], solutions[i], costs[i])

    writeInCsv(f"{OUTPUT_DIR:s}VNS_{n:03}_{int(PROB_EDGES*100):03}.csv", times, solutions, NUM_INSTANCES)


if __name__ == "__main__":
  main()
