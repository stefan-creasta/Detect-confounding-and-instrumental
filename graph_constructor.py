import numpy as np

class Node:
    def __init__(self, id, neighbors):
        self.id = id
        self.neighbors = neighbors
        self.fathers = []

class Edge:
    def __init__(self, node1, node2, type):
        self.node1 = node1
        self.node2 = node2
        self.type = type

def read_graph(fin):
    #reading n
    n = int(fin.readline())

    #reading the nodes, last one is confounding
    nodesList = fin.readline().split()
    d1 = {}
    revD1 = {}
    #list = []
    for i in range(n):
        d1[nodesList[i]] = i
        revD1[i] = nodesList[i]

    #edges are of three types: edges which do not change - type 0
    #                          edges which are either present, or not - type 1
    #                          edges which can change direction and be either present or not - type 2
    #reading type 0 of edges

    edges = []

    n1 = int(fin.readline())
    for i in range(n1):
        edgePair = fin.readline().split()
        edges.append(Edge(d1[edgePair[0]], d1[edgePair[1]], int(0)))

    #reading type 1 of edges

    n2 = int(fin.readline())
    for i in range(n2):
        edgePair = fin.readline().split()
        edges.append(Edge(d1[edgePair[0]], d1[edgePair[1]], int(1)))

    #reading type 2 of edges

    n3 = int(fin.readline())
    for i in range(n3):
        edgePair = fin.readline().split()
        edges.append(Edge(d1[edgePair[0]], d1[edgePair[1]], int(2)))
    return (n, edges, d1, revD1)

def construct_graph(edges, currentTypes, n):
    # constructing the normal graph
    list = []
    for i in range(n):
        list.append(Node(i, []))
    for j in range(len(edges)):
        first_node = list[edges[j].node1]
        second_node = list[edges[j].node2]
        if currentTypes[j] == 0:
            first_node.neighbors.append(second_node.id)
        if currentTypes[j] == 2:
            second_node.neighbors.append(first_node.id)

    for i in range(n): # constructing the mirrored graph
        list.append(Node(i + n, list[i].neighbors))
        node = list[i + n]
        new_neighbors = np.zeros(len(list[i].neighbors))
        for neighborId in range(len(node.neighbors)):
            new_neighbors[neighborId] = int(node.neighbors[neighborId] + n)
        node.neighbors = new_neighbors


    for i in range(n): # constructing the theta nodes
        list.append(Node(i + 2 * n, np.array([i, i + n])))

    for i in range(len(list)): # appending the parents
        for neighborId in list[i].neighbors:
            node = list[int(neighborId)]
            node.fathers.append(i)
    return list