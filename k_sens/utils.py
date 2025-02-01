import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mpl
from matplotlib import animation
import math
import csv
import random
NUM_NODES = [10, 20, 30, 50, 100, 200, 400]
PROB_EDGES = [0.01, 0.05, 0.1, 0.2, 0.5, 0.9]

def error(msg):
    print(msg)
    exit(1)

def readFromFile(filename):
    with open(filename, "r") as file:
        num_nodes, num_edges = [int(i) for i in file.readline().split()]
        G = nx.Graph()
        nodes = [int(i) for i in file.readline().split()]
        G.add_nodes_from(nodes)
        for i in range(num_edges):
            u, v = [int(e) for e in file.readline().split()]
            G.add_edge(u, v)
        file.readline()
        colors = [int(i) for i in file.readline().strip().split()]
        
        return G, colors
def writeInCsv(filename, times, solutions, num_instances):
    with  open(filename, "a") as csv_file:
        writer = csv.writer(csv_file)
        for i in range(num_instances):
            writer.writerow(['instance', 'time', 'solution len', 'solution'])
            writer.writerow([str(i), f'{times[i]}', str(len(solutions[i])), " ".join([str(j) for  j  in solutions[i]])])
        writer.writerow(["avg_time", str(sum(times)/len(times))])
        writer.writerow(["avg_length", str(sum([len(s)  for s in solutions])/len(solutions))])

def writeFitnessInCsv(filename, iter, solution, cost):
    with  open(filename, "a") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([iter,  " ".join([str(j) for j in solution]), cost])

def drawCircularGraph(G):
    nx.draw_circular(G, with_labels = True)

def savePlanarGraph(G, i):
    nx.draw_planar(G, with_labels = True)
    plt.savefig(f"G_{len(G.nodes):03}_{len(G.edges):03}_{i:02}.png")

def generateRandomGraph(n = 10, p = 0.01):
    return nx.erdos_renyi_graph(n, p, directed=False)

def generateInstances(n, p, num_instances = 25):
    return [generateRandomGraph(n, p) for i in range(num_instances)]

def colorGraph(G):
    delimeter = math.floor(len(G.nodes())/2)
    colors = [0]*(len(G.nodes) - delimeter) + [1]*delimeter
    random.shuffle(colors)
    reds_blues = [[i for i in range(len(colors)) if colors[i]==1], [i for i in range(len(colors)) if colors[i]==0]]
    return reds_blues

def writeInFile(filename, G, colors):
    with open(filename, "w") as file:
        num_nodes, num_edges = len(G.nodes), len(G.edges)
        file.write("{0:d} {1:d}".format(num_nodes, num_edges))
        file.write("\n")
        file.write(" ".join([str(i) for i in range(num_nodes)]))
        file.write("\n")
        edges = list(G.edges)
        for i in range(len(edges)):
            u, v = edges[i]
            file.write("{0:d} {1:d}\n".format(u, v))
        file.write("\n")
        reds, blues = colors
        colors_zeros_ones = [0]*num_nodes
        for r in reds:
           colors_zeros_ones[r] = 1

        file.write(" ".join([str(i) for i in colors_zeros_ones]))

def writeSolutionInFile(filename, time, solution, cost=0, k=2):

    with open(filename, 'a') as f:
        f.write("k:\n")
        f.write(str(k))
        f.write("solution:\n")
        for s in solution:
            f.write(f"{s:d} ")
        f.write("\n\n solution cost:\n")
        f.write(str(cost))
        f.write("\n\n num nodes in solution: \n")
        f.write(str(len(solution)))
        f.write("\n\n time:\n")
        f.write(str(time))

def drawColoredGraph(G, colors, name):
    reds, blues = colors
    pos = nx.circular_layout(G)  # positions for all nodes

    # nodes
    options = {"edgecolors": "tab:gray", "node_size": 800, "alpha": 0.9}
    nx.draw_networkx_nodes(G, pos, nodelist=reds, node_color="tab:red", **options)
    nx.draw_networkx_nodes(G, pos, nodelist=blues, node_color="tab:blue", **options)

    # edges
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    labels = {}
    for n in range(len(G.nodes)):
        labels[n] = str(n)

    nx.draw_networkx_labels(G, pos, labels, font_size=22, font_color="whitesmoke")
    plt.tight_layout()
    plt.axis("off")
    #plt.show()
    plt.savefig(name.replace("txt", "png"))
