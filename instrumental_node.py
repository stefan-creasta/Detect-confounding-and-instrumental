from graph_algorithms import can_get_to

import numpy as np

class InstrumentalInfo: # class which depicts the information we are interested in regarding the
    def __init__(self, Z, X, Y): # instrumental node
        self.Z = Z
        self.X = X
        self.Y = Y


# Method to read the info regarding the instrumental node
def read_instrumental_info(fin, d1):
    lis = fin.readline().split()
    return InstrumentalInfo(d1[lis[0]], d1[lis[1]], d1[lis[2]])

# Method to check whether there is an instrumental node in the graph
def is_instrumental(instrumental, list, n):
    for node in list[instrumental.Z].neighbors: # we must check that there is no edge between the
        if node == instrumental.Y: # instrumental and the end node
            return False
    thereIsEdge = False
    for node in list[instrumental.Z].neighbors: # we must check that there is an edge between the
        if node == instrumental.X: # instrumental and X
            thereIsEdge = True
    if thereIsEdge == False:
        return False
    if can_get_to_instrumental(instrumental, list, n) == True: # we must check whether we can get to Y
        return True # from the instrumental without the edge from Z to X
    return False

# Method for checking whether we can get from the instrumental node to the end node
def can_get_to_instrumental(instrumental, list, n):
    class NodeQueue:
        def __init__(self, nodeId, lastEdge): # last edge 1 if node---->child, 2 if node<----parent, 0 otherwise
            self.nodeId = nodeId
            self.lastEdge = lastEdge

    queue = []
    vizited = np.zeros(3 * n)
    vizited[instrumental.Z] = 1
    queue.append(NodeQueue(instrumental.Z, 0))
    are_independent = True
    while len(queue) > 0 and are_independent == True:
        currentNode = queue.pop(0)
        currentNodeId = currentNode.nodeId
        if currentNodeId >= n:
            continue
        if currentNodeId == instrumental.Y:
            are_independent = False
        for neighbor in list[currentNodeId].neighbors:
            if vizited[int(neighbor)] == 0:
                if (not(currentNodeId == instrumental.Z and neighbor == instrumental.X)):
                    queue.append(NodeQueue(int(neighbor), 1))
                    vizited[int(neighbor)] = 1
        canGoToParents = False
        lengthList = len(list[currentNodeId].fathers)
        lstEdge = currentNode.lastEdge
        if lengthList < 2 or lstEdge != 1: # we must check if there is just an upwards chain or if we didn't come from another parent
            canGoToParents = True
        else: # immorality detected
            canGoToParents = False
        if canGoToParents == True:
            for father in list[currentNodeId].fathers:
                if vizited[father] == 0:
                    queue.append(NodeQueue(father, 2))
                    vizited[father] = 1
    return are_independent
