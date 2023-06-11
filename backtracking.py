import numpy as np

from graph_constructor import construct_graph
from graph_algorithms import can_get_to, is_grand_child, find_cycle

# Defining the backtracking function
def backtracking(currentTypes, currentDsep, edges, start, end, d1, revD1, d_separation, n, fout):

    list = construct_graph(edges, currentTypes, n)

    blocked = np.zeros(3 * n)
    for i in range(len(d_separation)): # also blocking nodes part of the d-separation
        if currentDsep[i] == 1:
            blocked[d_separation[i]] = 1
            
    start_node = start # T_j
    end_node = end # Y_i

    are_independent = can_get_to(start_node, end_node, list, blocked, n)

    #if is_instrumental(d1["Z"], d1["Y"], list) == True:
    if find_cycle(list) == False and is_grand_child(d1["Y"], d1["T"], list) == False:
        for i in range(len(d_separation)): # also blocking nodes part of the d-separation
            if currentDsep[i] == 1:
                if d_separation[i] >= n: # printing the nodes part of the d_separation
                    fout.write(str(revD1[d_separation[i] - n]) + "_i ")
                else:
                    fout.write(str(revD1[d_separation[i]]) + "_j ")
        fout.write("||| ") # separate the graph print with the d_separation nodes by '|||'
        for i in range(n):
            for j in list[i].neighbors:
                fout.write(revD1[i] + "-" + revD1[j] + " ")
        fout.write(str(are_independent) + "\n")
    #print(are_independent)
    #print("is instrument: " + str(is_instrumental(d1["Z"], d1["Y"], list)))
    flagToStop = changing_current_d_sep(currentDsep, currentTypes, edges)
    if flagToStop == False:
        backtracking(currentTypes, currentDsep, edges, start, end, d1, revD1, d_separation, n, fout)

# Method to change the values for the d_sep nodes in the backtracking function
def changing_current_d_sep(currentDsep, currentTypes, edges):
    index = len(currentDsep) - 1
    flagToStop = False
    flagFound = False
    while flagToStop == False and flagFound == False:
        if index < 0:
            flagToStop = True
        else:
            currentDsep[index] += 1
            if currentDsep[index] > 1:
                currentDsep[index] = 0
                index -= 1
            else:
                flagFound = True
    if flagToStop == True:
        currentDsep = np.zeros(len(currentDsep))
        flagToStop = changing_current_types(currentTypes, edges)
    return flagToStop

# Method to change the values for the edges in the backtracking function
def changing_current_types(currentTypes, edges):
    index = len(currentTypes) - 1
    flagToStop = False
    flagFound = False
    while flagToStop == False and flagFound == False:
        if index < 0:
            flagToStop = True
        else:
            currentTypes[index] += 1
            if currentTypes[index] > edges[index].type:
                currentTypes[index] = 0
                index -= 1
            else:
                flagFound = True
    return flagToStop