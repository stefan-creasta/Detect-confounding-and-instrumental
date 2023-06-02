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

fin = open("input.txt", "r")
fout = open("output.txt", "w")

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

confounding = n - 1

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

#read the d-separation nodes
d_sep_size = int(fin.readline())
d_separation_string = fin.readline().split()
d_separation = []
for i in range(d_sep_size):
    currentNodes = d_separation_string[i].split("_")
    if currentNodes[1] == "j":
        d_separation.append(d1[currentNodes[0]])
    else:
        d_separation.append(d1[currentNodes[0]] + n)


currentTypes = np.zeros(len(edges))

sn_list = fin.readline().split("_")
sn = d1[sn_list[0]]
if sn_list[1] == "i":
    sn += n

en_list = fin.readline().split("_")
en = d1[en_list[0]]
if en_list[1] == "i":
    en += n

# Method of checking whether a node is ancestor of another node
def is_grand_child(start_node, end_node, list):
    class NodeQueue:
        def __init__(self, nodeId):
            self.nodeId = nodeId
    queue = []
    vizited = np.zeros(len(list))
    vizited[start_node] = 1
    queue.append(NodeQueue(start_node))
    found_node = False
    while len(queue) > 0 and found_node == False:
        node = queue.pop(0)
        for neighbor in list[int(node.nodeId)].neighbors:
            if neighbor == end_node:
                found_node = True
            if vizited[int(neighbor)] == 0:
                queue.append(NodeQueue(int(neighbor)))
                vizited[int(neighbor)] = 1
    return found_node

# Method of checking whether there is a cycle present
def find_cycle(list):
    class NodeQueue:
        def __init__(self, nodeId):
            self.nodeId = nodeId
    for currentNode in range(len(list)):
        queue = []
        vizited = np.zeros(len(list))
        vizited[currentNode] = 1
        queue.append(NodeQueue(currentNode))
        same_node = False
        while len(queue) > 0 and same_node == False:
            node = queue.pop(0)
            for neighbor in list[int(node.nodeId)].neighbors:
                if neighbor == currentNode:
                    same_node = True
                if vizited[int(neighbor)] == 0:
                    queue.append(NodeQueue(int(neighbor)))
                    vizited[int(neighbor)] = 1
        if same_node == True:
            return True
    return False

# Method for checking whether we can get from a start node to an end node
def can_get_to(start_node, end_node, list, blocked):
    class NodeQueue:
        def __init__(self, nodeId, lastEdge): # last edge 1 if node---->child, 2 if node<----parent, 0 otherwise
            self.nodeId = nodeId
            self.lastEdge = lastEdge

    queue = []
    vizited = np.zeros(3 * n)
    vizited[start_node] = 1
    queue.append(NodeQueue(start_node, 0))
    are_independent = True
    while len(queue) > 0 and are_independent == True:
        currentNode = queue.pop(0)
        currentNodeId = currentNode.nodeId
        if currentNodeId == end_node:
            are_independent = False
        if blocked[currentNodeId] == 0: # if the path is not blocked, we can go the children - chain
            for neighbor in list[currentNodeId].neighbors:
                if vizited[int(neighbor)] == 0:
                    queue.append(NodeQueue(int(neighbor), 1))
                    vizited[int(neighbor)] = 1
        canGoToParents = False
        lengthList = len(list[currentNodeId].fathers)
        lstEdge = currentNode.lastEdge
        if lengthList < 2 or lstEdge != 1: # we must check if there is just an upwards chain or if we didn't come from another parent
            if blocked[currentNodeId] == 0: # if it is an upwards chain, the path must not be blocked
                canGoToParents = True
        else: # immorality detected
            if blocked[currentNodeId] == 1: # we have to check if the node was selected in the d-separation in order to continue
                canGoToParents = True
        if canGoToParents == True:
            for father in list[currentNodeId].fathers:
                if vizited[father] == 0:
                    queue.append(NodeQueue(father, 2))
                    vizited[father] = 1
    return are_independent

# Method to check whether a start_node is instrumental, given a graph and a final "end_node"
def is_instrumental(start_node, end_node, list):
    for node in list[start_node].neighbors: # we check if there is a direct edge between the start node and the end node
        if node == end_node:
            return False # if there is, we stopped, as the node is not instrumental
    # 0 means no edge, 1 means from Z to U and 2 means from U to Z
    from_Z_to_U = 0
    # 0 means no edge, 1 means from Y to U and 2 means from U to Y
    from_Y_to_U = 0
    for node in list[start_node].neighbors:
        if node == confounding:
            from_Z_to_U = 1
    for node in list[confounding].neighbors:
        if node == start_node:
            from_Z_to_U = 2
    for node in list[confounding].neighbors:
        if node == end_node:
            from_Y_to_U = 2
    for node in list[end_node].neighbors:
        if node == confounding:
            from_Y_to_U = 1
    if not (from_Y_to_U == 0 or from_Z_to_U == 0 or (from_Y_to_U == 1 and from_Z_to_U == 1)): # either there is an edge missing, either there is an immorality present
        return False
    for node in list[start_node].fathers: # check if the instrument depends only on the theta or on confounding (as well)
        if node != confounding:
            if node != start_node + 2 * n:
                return False
    can_arrive = can_get_to(start_node, end_node, list, np.zeros(3 * n)) # the insturment is not independent of Y
    return not can_arrive

# Defining the backtracking function
def backtracking(currentTypes, start, end, ct):
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

    blocked = np.zeros(3 * n)
    for nodeId in d_separation: # also blocking nodes part of the d-separation
        blocked[nodeId] = 1

    start_node = start # T_j
    end_node = end # Y_i

    are_independent = can_get_to(start_node, end_node, list, blocked)


    #if is_instrumental(d1["Z"], d1["Y"], list) == True:
    if ct == 27:
        aaaa = 55
    if find_cycle(list) == False and is_grand_child(d1["Y"], d1["T"], list) == False:
        for i in range(n):
            for j in list[i].neighbors:
                fout.write(revD1[i] + "-" + revD1[j] + " ")
        fout.write(str(are_independent) + "\n")
    #print(are_independent)
    #print("is instrument: " + str(is_instrumental(d1["Z"], d1["Y"], list)))
    index = len(currentTypes) - 1
    flagToStop = False
    flagFound = False
    while flagToStop == False and flagFound == False:
        if index < 0:
            flagToStop = True
        currentTypes[index] += 1
        if currentTypes[index] > edges[index].type:
            currentTypes[index] = 0
            index -= 1
        else:
            flagFound = True
    if flagToStop == False:
        backtracking(currentTypes, start, end, ct + 1)
backtracking(currentTypes, sn, en, 1)
    
