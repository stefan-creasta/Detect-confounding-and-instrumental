from graph_algorithms import can_get_to
import numpy as np

# Method for reading the d-separation nodes and the start and end nodes
def read_d_separation_and_start_end(fin, n, d1):
    d_sep_size = int(fin.readline())
    d_separation_string = fin.readline().split()
    d_separation = []
    for i in range(d_sep_size):
        currentNodes = d_separation_string[i].split("_")
        if currentNodes[1] == "j":
            d_separation.append(d1[currentNodes[0]])
        else:
            d_separation.append(d1[currentNodes[0]] + n)
    sn = read_start_or_end_nodes(fin, d1, n)
    en = read_start_or_end_nodes(fin, d1, n)
    return (d_separation, sn, en)

def read_start_or_end_nodes(fin, d1, n):
    list_of_nodes = fin.readline().split(" ")
    nodes = []
    for elem in list_of_nodes:
        sn_list = elem.split("_")
        sn = d1[sn_list[0]]
        if sn_list[1] == "i" or sn_list[1] == "i\n":
            sn += n
        nodes.append(sn)
    return nodes
    
# Method to print and check whether the node is of i or j type
def printing(revD1, e, n, fout):
    if e >= n: 
        fout.write(str(revD1[e - n]) + "_i ")
    else:
        fout.write(str(revD1[e]) + "_j ")


# Method to check whether the d-separation is identical when you add the Z->Y edge or not
def check(initial_value, Z, Y, n, start_node, end_node, blocked, list):
    list[Z].neighbors = np.append(list[Z].neighbors, Y)
    #list[Y].fathers.append(Z)
    list[Y].fathers = np.append(list[Y].fathers, Z)
    #list[Z + n].neighbors.append(Y + n)
    list[Z + n].neighbors = np.append(list[Z + n].neighbors, Y + n)
    #list[Y + n].fathers.append(Z + n)
    list[Y + n].fathers = np.append(list[Y + n].fathers, Z + n)
    are_independent = can_get_to(start_node, end_node, list, blocked, n)
    list[Z].neighbors = np.delete(list[Z].neighbors, len(list[Z].neighbors) - 1)
    list[Y].fathers = np.delete(list[Y].fathers, len(list[Y].fathers) - 1)
    list[Z + n].neighbors = np.delete(list[Z + n].neighbors, len(list[Z + n].neighbors) - 1)
    list[Y + n].fathers = np.delete(list[Y + n].fathers, len(list[Y + n].fathers) - 1)
    return initial_value == are_independent