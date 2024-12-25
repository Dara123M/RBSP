import random
import itertools
from utils import *


def getNodesFromSolution(solution):
  return [i for i in range(len(solution)) if solution[i] == 1]

def getNeighDiff(G, coloring):
  reds, blues = coloring
  neigh_diff = {}
  for r in reds:
    r_closed_neighborhood = [node for node in G[r]]+[r]
    for b in blues:
      b_closed_neighborhood = [node for node in G[b]] + [b]
      rb_neighbors_diff = [node for node in r_closed_neighborhood if node not in G[b]]
      br_neighbors_diff = [node for node in b_closed_neighborhood if node not in G[r]]
      neighbors = set(rb_neighbors_diff + br_neighbors_diff)
      neigh_diff[(r,b)] = neighbors
  return neigh_diff

def getCoverage(neigh_diff, num_nodes):
  coverage = {}
  for n in range(num_nodes):
    coverage[n] = set()
  for pair, neighs in neigh_diff.items():
    for n in neighs:
      coverage[n].add(pair)

  return coverage

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

def getSeparateColors(coloring):
  reds = [i for i in range(len(coloring)) if coloring[i]==1]
  blues = [i for i in range(len(coloring)) if coloring[i]==0]
  return reds, blues

def getPairs(neigh_diff):
  pairs = []
  for pair in neigh_diff.keys():
    pairs.append(pair)

  return pairs

def checkConnectionsFaster(nodes_in_solution, pairs, coverageFull):
  cost = 0
  ins = set(itertools.chain.from_iterable([coverageFull[i] for i in nodes_in_solution]))
  cost = len(pairs) - len(ins)
  del(ins)
  return cost

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

