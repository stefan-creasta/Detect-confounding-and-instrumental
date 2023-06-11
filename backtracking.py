import numpy as np

from graph_constructor import construct_graph
from graph_algorithms import can_get_to, is_grand_child, find_cycle

# Defining the backtracking function
def backtracking(currentTypes, edges, start, end, d1, revD1, d_separation, n, fout):

    list = construct_graph(edges, currentTypes, n)

    blocked = np.zeros(3 * n)
    for nodeId in d_separation: # also blocking nodes part of the d-separation
        blocked[nodeId] = 1

    start_node = start # T_j
    end_node = end # Y_i

    are_independent = can_get_to(start_node, end_node, list, blocked, n)


    #if is_instrumental(d1["Z"], d1["Y"], list) == True:
    if find_cycle(list) == False and is_grand_child(d1["Y"], d1["T"], list) == False:
        for i in range(n):
            for j in list[i].neighbors:
                fout.write(revD1[i] + "-" + revD1[j] + " ")
        fout.write(str(are_independent) + "\n")
    #print(are_independent)
    #print("is instrument: " + str(is_instrumental(d1["Z"], d1["Y"], list)))
    flagToStop = changing_current_types(currentTypes, edges)
    if flagToStop == False:
        backtracking(currentTypes, edges, start, end, d1, revD1, d_separation, n, fout)

# Method to change the values for the edges in the backtracking function
def changing_current_types(currentTypes, edges):
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
    return flagToStop