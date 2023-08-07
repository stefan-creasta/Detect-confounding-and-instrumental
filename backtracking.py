import numpy as np

from graph_constructor import construct_graph
from graph_algorithms import cannot_get_to, is_grand_child, find_cycle
from instrumental_node import cannot_get_to_instrumental
from d_separation import printing, check

# The backtracking algorithm works as follows:
#       1) Encode the edge types (with values from 0 to a maximum of 2), d-separation nodes (with values from 0 to 1) and the start and end nodes (with indexes which will iterate the respective arrays)
#       2) Initialize the edge types, the nodes which are part of the d-separation, and the start and end nodes which will be checked during the independence test
#       3) Print the current start and end nodes
#       4) Print the current d-separation, alongside the edges which form the current graph
#       5) Try to move on to the next graph which can be created, by incrementing the next possible edge type without exceeding the limit associated with that edge type
#       6) If the next graph can be created, go back to step 4). Otherwise, reinitialize all edge types and continue with step 7)
#       7) Try to consider the next d-separation which can be created, by including the next possible node which has not been included before
#       8) If the next d-separation can be created, go back to step 4). Otherwise remove all the nodes from the current d-separation and continue with step 9)
#       9) Try to consider the next end node, by incrementing the index associated with it
#       10) If the next end node can be considered, go back to step 3). Otherwise reinitialize the index associated with the end node and continue with step 11)
#       11) Try to consider the next start node, by incrementing the index associated with it
#       12) If the next start node can be considered, go back to step 3). Otherwise the program terminates
# This represents the pseudocode of the backtracking algorithm. Comments in the functions below will describe in more detail how the iterations/incrementations for the edge types, d-separation nodes and start and end nodes work

# Defining the backtracking function, iterating over all the possible cases
def backtracking(instrumental, graph_details, current_graph_details, problem_setting, fout, limit_solutions, ct):

    # Storing the number of nodes in the graph in a separate variable
    n = graph_details.n

    # Define the current edges in the graph, at this point in the iteration, alongside the edges which connect the graph with the theta nodes and the mirrored graph
    current_edges = construct_graph(graph_details.edge_types, current_graph_details.current_edge_types, n)

    # Count all the nodes that are part of the current d-separation, at this point in the iteration
    nr_of_nodes_d_separation = 0

    # Initializing the array responsible for storing whether a node is conditioned on or not
    blocked = np.zeros(3 * n)

    # Condition on the nodes, which are part of the current d-separation
    for i in range(len(graph_details.d_separation)):
        if current_graph_details.current_d_separation[i] == 1:
            nr_of_nodes_d_separation += 1
            blocked[graph_details.d_separation[i]] = 1
            
    # Set the current start and end nodes
    start_node = graph_details.start_nodes[current_graph_details.index_start_nodes]
    end_node = graph_details.end_nodes[current_graph_details.index_end_nodes]

    # Compute the initial independence test, between the chosen start and end nodes
    are_independent = cannot_get_to(start_node, end_node, current_edges, blocked, n)

    # Compute the id of the graph, according to the current types of the edges
    graph_id = 0
    power3 = 1
    for i in range(len(current_graph_details.current_edge_types)):
        graph_id += current_graph_details.current_edge_types[len(current_graph_details.current_edge_types) - i - 1] * power3
        power3 *= 3

    # Check for the desired setting
    if problem_setting == "paper":
        if find_cycle(current_edges) == False and is_grand_child(graph_details.map_to_id["Y"], graph_details.map_to_id["T"], current_edges) == False: # Check for cycles and whether T happens before Y
            if nr_of_nodes_d_separation == 3: # Check whether the d-separation contains the correct number of nodes, just as in the paper - we are not interested in the d-separations which do not contain fewer nodes, for this particular setting
                for i in range(len(graph_details.d_separation)): # Print the nodes that are part of the d-separation
                    if current_graph_details.current_d_separation[i] == 1:
                        printing(graph_details.map_to_character, graph_details.d_separation[i], n, fout)
                fout.write("||| ") # Separate the d-separation from the graph edges in the output file by '|||'
                for i in range(n): # Print the edges
                    for j in current_edges[i].neighbors:
                        fout.write(graph_details.map_to_character[i] + "-" + graph_details.map_to_character[j] + " ")
                fout.write(str(are_independent) + " " + str(graph_id) + "\n") # Print the independence result, alongside the graph id

    elif problem_setting == "instrumental":
        if blocked[end_node] == False and blocked[start_node] == False and start_node != end_node: # Check whether the start and end nodes are identical or conditioned on
            if find_cycle(current_edges) == False: # Check for cycles
                if limit_solutions == False or check(are_independent, instrumental.Z, instrumental.Y, n, start_node, end_node, blocked, current_edges) == False: # Verify whether the output must only contain the cases for which there is a different outcome in the independence test by adding the Z-Y edge. If limit_solutions is set to False instead, print all of the possible cases
                    for i in range(len(graph_details.d_separation)): # Print the nodes that are part of the d-separation
                        if current_graph_details.current_d_separation[i] == 1:
                            printing(graph_details.map_to_character, graph_details.d_separation[i], n, fout)
                    fout.write("||| ") # Separate the d-separation from the graph edges in the output file by '|||'
                    for i in range(n): # Print the edges
                        for j in current_edges[i].neighbors:
                            fout.write(graph_details.map_to_character[i] + "-" + graph_details.map_to_character[j] + " ")
                    fout.write(str(check(are_independent, instrumental.Z, instrumental.Y, n, start_node, end_node, blocked, current_edges)) + " " + str(graph_id) + "\n") # Print the difference in the outcomes and graph id
    
    elif problem_setting == "multiple_confoundings":
        if blocked[end_node] == False and blocked[start_node] == False and start_node != end_node: # Check whether the start and end nodes are identical or conditioned on
            if find_cycle(current_edges) == False: # Check for cycles
                for i in range(len(graph_details.d_separation)): # Print the nodes that are part of the d-separation
                    if current_graph_details.current_d_separation[i] == 1:
                        printing(graph_details.map_to_character, graph_details.d_separation[i], n, fout)
                fout.write("||| ") # Separate the graph print with the d_separation nodes by '|||'
                for i in range(n): # Print the edges
                    for j in current_edges[i].neighbors:
                        fout.write(graph_details.map_to_character[i] + "-" + graph_details.map_to_character[j] + " ")
                fout.write(str(cannot_get_to_instrumental(instrumental, current_edges, n)) + " " + str(are_independent) + " " + str(graph_id) + "\n") # Print the two different independence tests and graph id
    
    print(ct) # Print the counter

    flagToStop = changing_current_types(graph_details, current_graph_details, n, fout) # Check whether all of the possible combinations have been tried
    if flagToStop == False: # If not, continue the iteration
        backtracking(instrumental, graph_details, current_graph_details, problem_setting, fout, limit_solutions, ct + 1)

# Method to change the values for the edge types in the backtracking function
def changing_current_types(graph_details, current_graph_details, n, fout): # First, we must iterate through all of the possible graphs
    index = len(current_graph_details.current_edge_types) - 1 # Try to change the last edge type initially
    flagToStop = False # Flag variable which signals when the whole array of edge types has been traversed
    flagFound = False # Flag variable, with the purpose of detecting the first edge type which can be changed
    while flagToStop == False and flagFound == False: # Iterate through the edge types, as long as no edge type which can be changed has been found
        if index < 0: # An index smaller than zero means that all of the edge types have been iterated through
            flagToStop = True # The flag must be changed
        else:
            current_graph_details.current_edge_types[index] += 1
            if current_graph_details.current_edge_types[index] > graph_details.edge_types[index].type: # Check whether it is viable to change the current edge type
                current_graph_details.current_edge_types[index] = 0 # If not, reset it
                index -= 1 # Decrease the index, moving on to the next edge type
            else:
                flagFound = True # The edge type has been found
    if flagToStop == True: # If all of the possible graphs have been considered, move on to the next d-separation. If not, go back to the backtracking function
        current_graph_details.current_edge_types = np.zeros(len(current_graph_details.current_edge_types)) # Reset all of the edge types
        flagToStop = changing_current_d_sep(graph_details, current_graph_details, n, fout)
    return flagToStop

# Method to change the values for the d-separation nodes
def changing_current_d_sep(graph_details, current_graph_details, n, fout): # We must iterate through all of the possible d-separations
    index = len(current_graph_details.current_d_separation) - 1 # Try to include the last node in the d-separation initially
    flagToStop = False # Flag variable which signals when the whole array of nodes which can be part of the d-separation, has been traversed
    flagFound = False # Flag variable, with the purpose of detecting the first node which can be included in the d-separation
    while flagToStop == False and flagFound == False: # Iterate through the nodes, as long as no new node which can be included in the d-separation has been found
        if index < 0: # An index smaller than zero means that all of the nodes have been iterated through
            flagToStop = True # The flag must be changed
        else:
            current_graph_details.current_d_separation[index] += 1
            if current_graph_details.current_d_separation[index] > 1: # Check whether the current node has already been included in the current d-separation
                current_graph_details.current_d_separation[index] = 0 # If it has been included, remove it from the current d-separation
                index -= 1 # Decrease the index, moving on to the next node
            else:
                flagFound = True # The node has been found and included in the current d-separation
    if flagToStop == True: # If all of the possible d-separations have been considered, move on to the next pair of start and end nodes. If not, go back to the backtracking function
        current_graph_details.current_d_separation = np.zeros(len(current_graph_details.current_d_separation)) # Remove all of the nodes from the current d-separation
        flagToStop = changing_current_start_and_end(graph_details, current_graph_details, n, fout)
    return flagToStop

# Method to change the current start and end nodes
def changing_current_start_and_end(graph_details, current_graph_details, n, fout): # Lastly, we must iterate through all of the possible pairs of start and end nodes
    if current_graph_details.index_end_nodes + 1 < len(graph_details.end_nodes): # Verify whether the next end node can be considered
        current_graph_details.index_end_nodes += 1 # Increment the index for the end node

        # Print the next pair of start and end nodes which is considered
        printing(graph_details.map_to_character, graph_details.start_nodes[current_graph_details.index_start_nodes], n, fout)
        printing(graph_details.map_to_character, graph_details.end_nodes[current_graph_details.index_end_nodes], n, fout)
        fout.write("\n")
        return False # The process has not yet finished, go back to the backtracking function
    else: # The index has arrived at the end of the array, and all of the end nodes have been considered. The next start node must be considered
        if current_graph_details.index_start_nodes + 1 < len(graph_details.start_nodes): # Verify whether the next start node can be considered
            current_graph_details.index_start_nodes += 1 # Increment the index for the start node
            current_graph_details.index_end_nodes = 0 # Reset the index for the end node

            # Print the next pair of start and end nodes which is considered
            printing(graph_details.map_to_character, graph_details.start_nodes[current_graph_details.index_start_nodes], n, fout)
            printing(graph_details.map_to_character, graph_details.end_nodes[0], n, fout)
            fout.write("\n")
            return False # The process has not yet finished, go back to the backtracking function
        else: # The index has arrived at the end of the array, and all of the start nodes have been considered. All of the possible cases have been checked and printed.
            return True # The process has finished