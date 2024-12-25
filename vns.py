from alg_utils import *
from copy import deepcopy
import datetime
import sys
import os
SOLUTION_PROB = 0.2
ITER_MAX = 500
K_MAX = 5
def initializeSolution(num_nodes, prob):
  solution = [0] * num_nodes
  for i in range(num_nodes):
    if random.random() < prob:
      solution[i] = 1

  return getNodesFromSolution(solution)

def shakeSolution(solution, num_nodes, k=1):
  
  nodesInSolution = deepcopy(solution)
  nodesNotInSolution = [i for i in range(num_nodes) if i not in nodesInSolution]
  random.shuffle(nodesInSolution)
  random.shuffle(nodesNotInSolution)

  if k > len(nodesInSolution):
    k = len(nodesInSolution)

  new_solution_nodes = nodesInSolution[0:len(nodesInSolution) - k] + nodesNotInSolution[0:k]
  

  return new_solution_nodes

def swapNodeInSolution(nodesInSolution, node):
  nodesCopy = deepcopy(nodesInSolution)
  if node in nodesCopy:
    nodesCopy.remove(node)
  else:
    nodesCopy.append(node)
  return nodesCopy

def localSearchFirstImproved(solution, pairs, neigh_diff, coverageFull, num_nodes):

  improved = True
  new_solution_nodes = deepcopy(solution)
  new_solution_num_nodes = len(new_solution_nodes)
  new_solution_cost = checkConnectionsFaster(new_solution_nodes, pairs, coverageFull)
  all_nodes = [i for i in range(num_nodes)]
  while improved:
    improved = False
    random.shuffle(all_nodes)
    for node in all_nodes:
      current_solution_nodes = swapNodeInSolution(new_solution_nodes, node)
      current_solution_cost = checkConnectionsFaster(current_solution_nodes, pairs, coverageFull)
      if (current_solution_cost, len(current_solution_nodes)) < (new_solution_cost, new_solution_num_nodes):
        improved = True
        new_solution_nodes = deepcopy(current_solution_nodes)
        new_solution_num_nodes = len(current_solution_nodes)
        new_solution_cost = current_solution_cost
        break

  return new_solution_nodes, new_solution_cost

def variableNeighborhoodSearch(G, coloring, num_nodes, iter_max, k_max):
  solution = initializeSolution(num_nodes, SOLUTION_PROB)

  neigh_diff = getNeighDiff(G, coloring)
  pairs = getPairs(neigh_diff)
  coverageFull = getCoverage(neigh_diff, num_nodes)
  cost = checkConnectionsFaster(solution, pairs, coverageFull)

  iter = 1
  k = 1
  while iter < iter_max:

    if iter%100==1:
      print(f"iteration: {iter}\n solution:\n {solution}\n cost: {cost}")
    iter += 1

    new_solution = shakeSolution(solution, num_nodes, k)

    solutionLocalSearch, solutionLocalSearchCost = localSearchFirstImproved(new_solution, pairs, neigh_diff, coverageFull, num_nodes)

    if (cost, len(solution)) > (solutionLocalSearchCost, len(solutionLocalSearch)) or ((cost, len(solution)) == (solutionLocalSearchCost, len(solutionLocalSearch)) and random.random()<0.2):
      solution = deepcopy(solutionLocalSearch)
      cost = solutionLocalSearchCost
      k = 1
    else:
      k += 1
      if k > k_max:
         k = 1
     
  return sorted(solution), cost

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
  oFiles = [OUTPUT_DIR+f.replace("graph", "vns") for f in filesWithSpecs]

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

      solution, cost = variableNeighborhoodSearch(instances[i][0], instances[i][1], NUM_NODES, ITER_MAX, K_MAX)
      end_time = datetime.datetime.now()
      times.append((end_time-start_time).total_seconds())
      solutions.append(solution)
      costs.append(cost)
      writeSolutionInFile(oFiles[i], times[i], solutions[i], costs[i])

  writeInCsv(f"{OUTPUT_DIR:s}VNS_{NUM_NODES:03}_{int(PROB_EDGES*100):03}.csv", times, solutions, NUM_INSTANCES)


if __name__ == "__main__":
  main()
