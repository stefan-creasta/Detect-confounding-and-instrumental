import numpy as np

from graph_constructor import construct_graph
from graph_algorithms import can_get_to, is_grand_child, find_cycle
from instrumental_node import is_instrumental
from d_separation import printing, check

# Defining the backtracking function
def backtracking(instrumental, currentTypes, currentDsep, edges, start_nodes, end_nodes, index_start, index_end, d1, revD1, d_separation, n, fout, limit_solutions, ct):

    list = construct_graph(edges, currentTypes, n)

    #for node in list[d1['V']].fathers:
    #    if node == d1['Z'] or node == d1['U']:
    #        ct += 1
    if ct == 500:
        aaaa = 5
    blocked = np.zeros(3 * n)
    for i in range(len(d_separation)): # also blocking nodes part of the d-separation
        if currentDsep[i] == 1:
            blocked[d_separation[i]] = 1
            
    start_node = start_nodes[index_start] # T_j
    end_node = end_nodes[index_end] # Y_i

    if start_node == 2 and end_node == 0 and blocked[1] == 1:
        aaaaaaa = 5

    are_independent = can_get_to(start_node, end_node, list, blocked, n)

    if is_instrumental(instrumental, list, n) == True and blocked[end_node] == False and blocked[start_node] == False:
        if find_cycle(list) == False: #and is_grand_child(d1["Y"], d1["T"], list) == False:
            if limit_solutions == False or check(are_independent, instrumental.Z, instrumental.Y, n, start_node, end_node, blocked, list) == False:
                for i in range(len(d_separation)): # also blocking nodes part of the d-separation
                    if currentDsep[i] == 1:
                        printing(revD1, d_separation[i], n, fout)
                fout.write("||| ") # separate the graph print with the d_separation nodes by '|||'
                for i in range(n):
                    for j in list[i].neighbors:
                        fout.write(revD1[i] + "-" + revD1[j] + " ")
                fout.write(str(are_independent) + "\n")
    #print(are_independent)
    #print("is instrument: " + str(is_instrumental(d1["Z"], d1["Y"], list)))
    print(ct)
    (flagToStop, index_start, index_end) = changing_current_d_sep(currentDsep, currentTypes, edges, start_nodes, end_nodes, index_start, index_end, revD1, n, fout)
    if flagToStop == False:
        backtracking(instrumental, currentTypes, currentDsep, edges, start_nodes, end_nodes, index_start, index_end, d1, revD1, d_separation, n, fout, limit_solutions, ct + 1)

# Method to change the values for the d_sep nodes in the backtracking function
def changing_current_d_sep(currentDsep, currentTypes, edges, sn, en, index_start, index_end, d1, n, fout):
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
        (flagToStop, index_start, index_end) = changing_current_types(currentTypes, edges, sn, en, index_start, index_end, d1, n, fout)
    return (flagToStop, index_start, index_end)

# Method to change the values for the edges in the backtracking function
def changing_current_types(currentTypes, edges, sn, en, index_start, index_end, d1, n, fout):
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
    if flagToStop == True:
        currentTypes = np.zeros(len(currentTypes))
        (flagToStop, index_start, index_end) = changing_current_start_and_end(sn, en, index_start, index_end, d1, n, fout)
    return (flagToStop, index_start, index_end)

# Method to change the current start and end nodes
def changing_current_start_and_end(sn, en, index_start, index_end, d1, n, fout):
    if index_end + 1 < len(en): # if the end node can be moved, move it
        printing(d1, sn[index_start], n, fout)
        printing(d1, en[index_end + 1], n, fout)
        fout.write("\n")
        return (False, index_start, index_end + 1)
    else:
        if index_start + 1 < len(sn): # if the start node can be moved, move it
            printing(d1, sn[index_start + 1], n, fout)
            printing(d1, en[0], n, fout)
            fout.write("\n")
            return (False, index_start + 1, 0) # reset the end node
        else:
            return (True, 0, 0) # the process has finished