import numpy as np

class Node:
    def __init__(self, id, neighbors):
        self.id = id # The id of the node, as it was defined in the dictionary
        self.neighbors = neighbors # The neighbors, or the children of the node
        self.fathers = [] # The parents of the node

class Edge:
    def __init__(self, node1, node2, type):
        self.node1 = node1 # The first node which creates the edge
        self.node2 = node2 # The second node which creates the edge
        self.type = type # The edge type

# Method for reading the nodes and edges present in the input file, and storing them
def read_graph(fin):
    # Read n
    n = int(fin.readline())

    # Read the nodes, last one is confounding. For the multiple confoundings input, the last two nodes will represent the confoundings
    nodesList = fin.readline().split()
    d1 = {}
    revD1 = {}

    for i in range(n):
        d1[nodesList[i]] = i
        revD1[i] = nodesList[i]

    # Edges are of three types: edges which do not change - type 0
    #                           edges which are either present, or not - type 1
    #                           edges which can present, reversed or absent - type 2
    # Read type 0 of edges

    edges = []

    n1 = int(fin.readline())
    for i in range(n1):
        edgePair = fin.readline().split() # Each edge can be found on a separate line
        edges.append(Edge(d1[edgePair[0]], d1[edgePair[1]], int(0)))

    # Read type 1 of edges

    n2 = int(fin.readline())
    for i in range(n2):
        edgePair = fin.readline().split() # Each edge can be found on a separate line
        edges.append(Edge(d1[edgePair[0]], d1[edgePair[1]], int(1)))

    # Read type 2 of edges

    n3 = int(fin.readline())
    for i in range(n3):
        edgePair = fin.readline().split() # Each edge can be found on a separate line
        edges.append(Edge(d1[edgePair[0]], d1[edgePair[1]], int(2)))
    return (n, edges, d1, revD1)

# In the program, the nodes will be represented by their dictionary id. The initial nodes will have an id between 0 and n - 1. The nodes from the mirrored graph will have ids between n and 2*n - 1. The theta nodes will have ids between 2*n and 3*n - 1
# Method which constructs the current graph, alongside the theta nodes and the mirrored graph, just as in the paper
def construct_graph(edges, currentTypes, n):
    # Define the list of edges
    list = []
    for i in range(n): # Construct the normal graph
        list.append(Node(i, []))
    for j in range(len(edges)):
        first_node = list[edges[j].node1]
        second_node = list[edges[j].node2]
        if currentTypes[j] == 0:
            first_node.neighbors.append(second_node.id) # Type 0 implies the regular edge
        if currentTypes[j] == 2:
            second_node.neighbors.append(first_node.id) # Type 2 implies the reversed edge

    for i in range(n): # Construct the mirrored graph
        list.append(Node(i + n, list[i].neighbors))
        node = list[i + n]
        new_neighbors = np.zeros(len(list[i].neighbors))
        for neighborId in range(len(node.neighbors)):
            new_neighbors[neighborId] = int(node.neighbors[neighborId] + n)
        node.neighbors = new_neighbors


    for i in range(n): # Construct the theta nodes
        list.append(Node(i + 2 * n, np.array([i, i + n])))

    for i in range(len(list)): # Append the parents
        for neighborId in list[i].neighbors:
            node = list[int(neighborId)]
            node.fathers.append(i)
    return list