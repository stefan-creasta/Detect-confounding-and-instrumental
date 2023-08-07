from graph_algorithms import cannot_get_to
from graph_constructor import Node
import numpy as np

class InstrumentalInfo: # class which depicts the information we are interested in regarding the
    def __init__(self, Z, X, Y):
        self.Z = Z # Instrumental variable
        self.X = X # Explanatory variable
        self.Y = Y # Dependent variable


# Method to read the info regarding the instrumental node
def read_instrumental_info(fin, d1):
    lis = fin.readline().split()
    return InstrumentalInfo(d1[lis[0]], d1[lis[1]], d1[lis[2]])

# Method to check whether there is an instrumental node in the graph
def is_instrumental(instrumental, list, n):
    for node in list[instrumental.Z].neighbors: # We must check that there is no edge between the instrument and the outcome
        if node == instrumental.Y:
            return False
    if Z_X_independent(instrumental, list, n) == True: # Check whether Z and X are independent
        return False
    if cannot_get_to_instrumental(instrumental, list, n) == True: # Check whether we can get to Y from the instrumental without all the incoming edges to X
        return True
    return False

# Method for checking whether Z and X are independent
def Z_X_independent(instrumental, list, n):
    new_list = [] # Create the new list of edges, without nodes with id greater than n
    for i in range(n):
        new_list.append(Node(i, []))
    for current_node in new_list:
        for neighbor in list[current_node.id].neighbors:
            if neighbor < n:
                current_node.neighbors.append(neighbor)
                new_list[neighbor].fathers.append(current_node.id)
    return cannot_get_to(instrumental.Z, instrumental.X, new_list, np.zeros(n), n)

# Method for checking whether we can get from the instrumental node to the end node
def cannot_get_to_instrumental(instrumental, list, n):
    new_list = [] # Create the new list of edges, and remove any incoming edges to X
    for i in range(n):
        new_list.append(Node(i, []))
    for current_node in new_list:
        for neighbor in list[current_node.id].neighbors:
            if neighbor != instrumental.X and neighbor < n:
                current_node.neighbors.append(neighbor)
                new_list[neighbor].fathers.append(current_node.id)
    return cannot_get_to(instrumental.Z, instrumental.Y, new_list, np.zeros(n), n)
