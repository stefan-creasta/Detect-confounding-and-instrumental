import numpy as np

from graph_constructor import construct_graph
from graph_algorithms import cannot_get_to, is_grand_child, find_cycle
from instrumental_node import is_instrumental, cannot_get_to_instrumental
from d_separation import printing, check

# Defining the backtracking function
def backtracking(instrumental, graph_details, current_graph_details, fout, limit_solutions, ct):

    n = graph_details.n

    current_edges = construct_graph(graph_details.edge_types, current_graph_details.current_edge_types, n)

    if ct == 500:
        aaaa = 5
    blocked = np.zeros(3 * n)
    sum = 0
    for i in range(len(graph_details.d_separation)): # also blocking nodes part of the d-separation
        if current_graph_details.current_d_separation[i] == 1:
            sum += 1
            blocked[graph_details.d_separation[i]] = 1
            
    start_node = graph_details.starting_nodes[current_graph_details.index_starting_nodes]
    end_node = graph_details.ending_nodes[current_graph_details.index_ending_nodes]

    are_independent = cannot_get_to(start_node, end_node, current_edges, blocked, n)

    graph_id = 0
    power3 = 1
    for i in range(len(current_graph_details.current_edge_types)):
        graph_id += current_graph_details.current_edge_types[len(current_graph_details.current_edge_types) - i - 1] * power3
        power3 *= 3

    if blocked[end_node] == False and blocked[start_node] == False and start_node != end_node:
        if find_cycle(current_edges) == False: #and is_grand_child(d1["Y"], d1["T"], current_edges) == False:
            if limit_solutions == False and graph_id == 4 and cannot_get_to_instrumental(instrumental, current_edges, n) == are_independent: #or check(are_independent, instrumental.Z, instrumental.Y, n, start_node, end_node, blocked, current_edges) == False:
                for i in range(len(graph_details.d_separation)): # also blocking nodes part of the d-separation
                    if current_graph_details.current_d_separation[i] == 1:
                        printing(graph_details.map_to_character, graph_details.d_separation[i], n, fout)
                fout.write("||| ") # separate the graph print with the d_separation nodes by '|||'
                for i in range(n):
                    for j in current_edges[i].neighbors:
                        fout.write(graph_details.map_to_character[i] + "-" + graph_details.map_to_character[j] + " ")
                #for i in range(len(current_graph_details.current_edge_types)):
                #    fout.write(str(current_graph_details.current_edge_types[i]) + " ")
                fout.write(str(cannot_get_to_instrumental(instrumental, current_edges, n)) + " " + str(are_independent) + " " + str(graph_id) + "\n")
                #if cannot_get_to_instrumental(instrumental, current_edges, n) == are_independent:
                #    fout.write("True" + "\n")
                #else:
                #    fout.write("False" + "\n")
    #print(are_independent)
    #print("is instrument: " + str(is_instrumental(d1["Z"], d1["Y"], current_edges)))
    print(ct)
    flagToStop = changing_current_types(graph_details, current_graph_details, n, fout)
    if flagToStop == False:
        backtracking(instrumental, graph_details, current_graph_details, fout, limit_solutions, ct + 1)

# Method to change the values for the edge types in the backtracking function
def changing_current_types(graph_details, current_graph_details, n, fout):
    index = len(current_graph_details.current_edge_types) - 1
    flagToStop = False
    flagFound = False
    while flagToStop == False and flagFound == False:
        if index < 0:
            flagToStop = True
        else:
            current_graph_details.current_edge_types[index] += 1
            if current_graph_details.current_edge_types[index] > graph_details.edge_types[index].type:
                current_graph_details.current_edge_types[index] = 0
                index -= 1
            else:
                flagFound = True
    if flagToStop == True:
        current_graph_details.current_edge_types = np.zeros(len(current_graph_details.current_edge_types))
        flagToStop = changing_current_d_sep(graph_details, current_graph_details, n, fout)
    return flagToStop

# Method to change the values for the d_sep nodes in the backtracking function
def changing_current_d_sep(graph_details, current_graph_details, n, fout):
    index = len(current_graph_details.current_d_separation) - 1
    flagToStop = False
    flagFound = False
    while flagToStop == False and flagFound == False:
        if index < 0:
            flagToStop = True
        else:
            current_graph_details.current_d_separation[index] += 1
            if current_graph_details.current_d_separation[index] > 1:
                current_graph_details.current_d_separation[index] = 0
                index -= 1
            else:
                flagFound = True
    if flagToStop == True:
        current_graph_details.current_d_separation = np.zeros(len(current_graph_details.current_d_separation))
        flagToStop = changing_current_start_and_end(graph_details, current_graph_details, n, fout)
    return flagToStop

# Method to change the current start and end nodes
def changing_current_start_and_end(graph_details, current_graph_details, n, fout):
    if current_graph_details.index_ending_nodes + 1 < len(graph_details.ending_nodes): # if the end node can be moved, move it
        current_graph_details.index_ending_nodes += 1
        printing(graph_details.map_to_character, graph_details.starting_nodes[current_graph_details.index_starting_nodes], n, fout)
        printing(graph_details.map_to_character, graph_details.ending_nodes[current_graph_details.index_ending_nodes], n, fout)
        fout.write("\n")
        return False
    else:
        if current_graph_details.index_starting_nodes + 1 < len(graph_details.starting_nodes): # if the start node can be moved, move it
            current_graph_details.index_starting_nodes += 1
            current_graph_details.index_ending_nodes = 0 # reset the end node
            printing(graph_details.map_to_character, graph_details.starting_nodes[current_graph_details.index_starting_nodes], n, fout)
            printing(graph_details.map_to_character, graph_details.ending_nodes[0], n, fout)
            fout.write("\n")
            return False
        else:
            return True # the process has finished