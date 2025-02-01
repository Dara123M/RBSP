import random
import itertools
from utils import *

def getPairs(neigh_diff):
  pairs = []
  for pair in neigh_diff.keys():
    pairs.append(pair)

  return pairs
def getSeparateColors(coloring):
  reds = {i for i in range(len(coloring)) if coloring[i]==1}
  blues = {i for i in range(len(coloring)) if coloring[i]==0}
  return reds, blues

def getNodesFromSolution(solution):
  return [i for i in range(len(solution)) if solution[i] == 1]

def getNeighDiff(G, coloring):
    reds, blues = coloring
    neigh_diff = {}

    closed_neighborhoods = {}
    for r in reds:
        closed_neighborhoods[r] = set(G[r]) | {r}
    for b in blues:
        closed_neighborhoods[b] = set(G[b]) | {b}
    
    for r in reds:
        for b in blues:
            rb_neighbors_diff = closed_neighborhoods[r] - set(G[b])
            br_neighbors_diff = closed_neighborhoods[b] - set(G[r])
            neigh_diff[(r, b)] = rb_neighbors_diff | br_neighbors_diff
    
    return neigh_diff

def getCoverage(neigh_diff, num_nodes):
    coverage = {n: set() for n in range(num_nodes)}
    
    for pair, neighs in neigh_diff.items():
        for n in neighs:
            coverage[n].add(pair)
    
    return coverage

def checkConnectionsFaster(nodes_in_solution, pairs, coverageFull):

    covered_pairs = set()

    for node in nodes_in_solution:
        covered_pairs.update(coverageFull[node])

    
    return len(pairs) - len(covered_pairs)


def coverageSolution(nodes_in_solution, coverageFull):
  covers ={}
  for node in nodes_in_solution:
    covers[node] = coverageFull[node]

  return covers

def non_coverage(nodes_in_solution, neigh_diff):
  non_covers = set()
  for pair, neighs in neigh_diff.items():
    intersection = [node for node in nodes_in_solution if node in neighs]
    if intersection == []:
      non_covers.add(pair)

  return non_covers


def checkConnectionsFaster_slow(nodes_in_solution, pairs, neigh_diff):
  cost = 0

  for p in pairs:
    hasConnections = False
    neighbors = neigh_diff[p]
    for neighbor in neighbors:
      if neighbor in nodes_in_solution:
        hasConnections = True
        break
    if not hasConnections:
      cost += 1

  return cost

