import numpy as np

# Method of checking whether a node is grand-child of another node - checking whether a factor occured before another one
def is_grand_child(start_node, end_node, list): # The approach is to utilize the Breadth First Search algorithm
    class NodeQueue:
        def __init__(self, nodeId):
            self.nodeId = nodeId # The id of the node, as it was defined in the dictionary
    queue = []
    vizited = np.zeros(len(list)) # No node has been currently visited
    vizited[start_node] = 1 # Start the process, by visiting the start node
    queue.append(NodeQueue(start_node))
    found_node = False # Flag variable which signals when the algorithm has reached the end node
    while len(queue) > 0 and found_node == False:
        node = queue.pop(0)
        for neighbor in list[int(node.nodeId)].neighbors:
            if neighbor == end_node:
                found_node = True # If the algorithm has reached the end node, the end node is indeed the grand-child of the start node
            if vizited[int(neighbor)] == 0:
                queue.append(NodeQueue(int(neighbor)))
                vizited[int(neighbor)] = 1 # Visit the current node
    return found_node

# Method of checking whether there is a cycle present
def find_cycle(list): # The approach is to apply the Breadth First Search algorithm on every node, and verify whether the current node can reach itself
    class NodeQueue:
        def __init__(self, nodeId):
            self.nodeId = nodeId # The id of the node, as it was defined in the dictionary
    for currentNode in range(len(list)): # Take every node into consideration
        queue = []
        vizited = np.zeros(len(list)) # No node has been currently visited
        vizited[currentNode] = 1 # Start the process, by visiting the current node
        queue.append(NodeQueue(currentNode))
        same_node = False # Flag variable which signals when the algorithm has reached the current node and thus, detecting a cycle in the graph
        while len(queue) > 0 and same_node == False:
            node = queue.pop(0)
            for neighbor in list[int(node.nodeId)].neighbors:
                if neighbor == currentNode:
                    same_node = True # If the algorithm has reached the current node, the graph contains a cycle
                if vizited[int(neighbor)] == 0:
                    queue.append(NodeQueue(int(neighbor)))
                    vizited[int(neighbor)] = 1 # Visit the node
        if same_node == True:
            return True # No need to continue further, the graph is not acyclic
    return False

# Method for checking whether we can get from a start node to an end node
def cannot_get_to(start_node, end_node, list, blocked, n): # The approach is to apply the Breadth First Search algorithm, while taking into consideraiton the properties of Bayesian networks
    class NodeQueue:
        def __init__(self, nodeId, lastEdge):
            self.nodeId = nodeId # The id of the node, as it was defined in the dictionary
            self.lastEdge = lastEdge # Last edge is 1 if the edge has been of the form node---->child, 2 for node<----parent, 0 otherwise

    queue = []
    # Two vizited arrays will be used, one for normal paths and the other for paths which at that moment included an immorality
    # Initialize the two vizited arrays
    vizited_immorality = np.zeros(3 * n)
    vizited_normally = np.zeros(3 * n)
    # Start the process by first viziting the start node
    vizited_immorality[start_node] = 1
    vizited_normally[start_node] = 1
    queue.append(NodeQueue(start_node, 0))
    # First, consider that the two nodes are independent
    are_independent = True
    while len(queue) > 0 and are_independent == True: # Stop the program when all of the possible paths which canbe visited have been exhausted or when the two nodes are not independent
        currentNode = queue.pop(0)
        currentNodeId = currentNode.nodeId
        if currentNodeId == end_node: # If the current node is the end node, there is a path from the start node to the end node
            are_independent = False # The two nodes are not independent
        if blocked[currentNodeId] == 0: # If the path is not blocked, we can go to the children - chain
            for neighbor in list[currentNodeId].neighbors:
                if vizited_normally[int(neighbor)] == 0:
                    vizited_normally[int(neighbor)] = 1 # Visit the node
                    queue.append(NodeQueue(int(neighbor), 1))
        canGoToParents = False
        lengthList = len(list[currentNodeId].fathers)
        lstEdge = currentNode.lastEdge
        if lengthList < 2 or lstEdge != 1: # We must check if there is just an upwards chain or if we didn't come from another parent
            if blocked[currentNodeId] == 0: # If it is an upwards chain, the path must not be blocked
                canGoToParents = True
        else: # Immorality detected
            if blocked[currentNodeId] == 1: # We have to check if the node was selected in the d-separation in order to continue
                canGoToParents = True
        if canGoToParents == True:
            for father in list[currentNodeId].fathers:
                if vizited_immorality[int(father)] == 0:
                    queue.append(NodeQueue(father, 2))
                    vizited_immorality[father] = 1 # Visit the node
    return are_independent
