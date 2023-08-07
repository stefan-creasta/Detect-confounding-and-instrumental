from graph_algorithms import cannot_get_to
import numpy as np

# Method for reading the d-separation nodes and the start and end nodes
def read_d_separation_and_start_end(fin, n, d1):
    # Read the d-separation nodes, which are separated by ' ' on a single line
    d_sep_size = int(fin.readline())
    d_separation_string = fin.readline().split()
    d_separation = []
    for i in range(d_sep_size):
        currentNodes = d_separation_string[i].split("_")
        if currentNodes[1] == "j": # If the node ends with 'j', it has the same id as in the dictionary
            d_separation.append(d1[currentNodes[0]])
        else: # Otherwise, it ends with 'i', and the number of nodes must be added to the id
            d_separation.append(d1[currentNodes[0]] + n)

    # Read the start and end nodes
    sn = read_start_or_end_nodes(fin, d1, n) # First the start nodes
    en = read_start_or_end_nodes(fin, d1, n) # Then the end nodes
    return (d_separation, sn, en)

# Method to read the start or end nodes
def read_start_or_end_nodes(fin, d1, n):
    # Read the start or end ndoes, which are separated by ' ' on a single line
    list_of_nodes = fin.readline().split(" ")
    nodes = []
    for elem in list_of_nodes:
        sn_list = elem.split("_")
        sn = d1[sn_list[0]] # If the node ends with 'j', it has the same id as in the dictionary
        if sn_list[1] == "i" or sn_list[1] == "i\n": # Otherwise, it ends with 'i', and the number of nodes must be added to the id
            sn += n
        nodes.append(sn)
    return nodes
    
# Method to check whether the node is part of the mirrored graph or not, and print it accordingly
def printing(revD1, e, n, fout):
    if e >= n: 
        fout.write(str(revD1[e - n]) + "_i ")
    else:
        fout.write(str(revD1[e]) + "_j ")


# Method to check whether the independence test has the same outcome you add the Z-Y edge
def check(initial_value, Z, Y, n, start_node, end_node, blocked, list):
    # First add the edge in the regular graph
    list[Z].neighbors = np.append(list[Z].neighbors, Y)
    list[Y].fathers = np.append(list[Y].fathers, Z)
    # Then add the edge in the mirrored graph
    list[Z + n].neighbors = np.append(list[Z + n].neighbors, Y + n)
    list[Y + n].fathers = np.append(list[Y + n].fathers, Z + n)
    # Find the result of the independence test
    are_independent = cannot_get_to(start_node, end_node, list, blocked, n)
    # Remove the edge in the regular graph
    list[Z].neighbors = np.delete(list[Z].neighbors, len(list[Z].neighbors) - 1)
    list[Y].fathers = np.delete(list[Y].fathers, len(list[Y].fathers) - 1)
    # Remove the edge in the mirrored graph
    list[Z + n].neighbors = np.delete(list[Z + n].neighbors, len(list[Z + n].neighbors) - 1)
    list[Y + n].fathers = np.delete(list[Y + n].fathers, len(list[Y + n].fathers) - 1)
    # If the independence tests have the same outcome, True will be returned
    return initial_value == are_independent