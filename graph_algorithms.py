import numpy as np

# Method of checking whether a node is grand-child of another node
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
def can_get_to(start_node, end_node, list, blocked, n):
    class NodeQueue:
        def __init__(self, nodeId, lastEdge): # last edge 1 if node---->child, 2 if node<----parent, 0 otherwise
            self.nodeId = nodeId
            self.lastEdge = lastEdge

    queue = []
    vizited_normally = np.zeros(3 * n)
    vizited_blocked = np.zeros(3 * n)
    vizited_normally[start_node] = 1
    vizited_blocked[start_node] = 1
    queue.append(NodeQueue(start_node, 0))
    are_independent = True
    while len(queue) > 0 and are_independent == True:
        currentNode = queue.pop(0)
        currentNodeId = currentNode.nodeId
        if currentNodeId == end_node:
            are_independent = False
        if blocked[currentNodeId] == 0: # if the path is not blocked, we can go the children - chain
            for neighbor in list[currentNodeId].neighbors:
                if vizited_blocked[int(neighbor)] == 0:
                    vizited_blocked[int(neighbor)] = 1
                    #vizited_blocked[int(neighbor)] = 1
                    queue.append(NodeQueue(int(neighbor), 1))
        canGoToParents = False
        lengthList = len(list[currentNodeId].fathers)
        lstEdge = currentNode.lastEdge
        normally = True
        if lengthList < 2 or lstEdge != 1: # we must check if there is just an upwards chain or if we didn't come from another parent
            if blocked[currentNodeId] == 0: # if it is an upwards chain, the path must not be blocked
                canGoToParents = True
        else: # immorality detected
            if blocked[currentNodeId] == 1: # we have to check if the node was selected in the d-separation in order to continue
                canGoToParents = True
                normally = False
        if canGoToParents == True:
            for father in list[currentNodeId].fathers:
                if vizited_normally[int(father)] == 0:
                    queue.append(NodeQueue(father, 2))
                    vizited_normally[father] = 1
    return are_independent
