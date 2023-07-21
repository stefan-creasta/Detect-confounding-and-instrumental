# Class dedicated for storing the graph details present in the input file
class GraphDetails:
    def __init__(self, n, edge_types, map_to_id, map_to_character, d_separation, starting_nodes, ending_nodes):
        self.n = n # assigning the number of nodes, having ids from 0 to n - 1
        self.edge_types = edge_types # assigning the different types of edges that this graph can have
        self.map_to_id = map_to_id # assigning the dictionary responsible for converting chatacters to ids
        self.map_to_character = map_to_character # assigning the dictionary responsible for converting ids to chatacters
        self.d_separation = d_separation # assigning all of the possible nodes that can be part of a d-separation
        self.starting_nodes = starting_nodes # assigning all of the possible nodes that can be starting node
        self.ending_nodes = ending_nodes # assigning all of the possible nodes that can be ending nodes

# Class dedicated for storing details regarding the current graph details, which are to be computed at the next iteration in the backtracking function
class CurrentGraphDetails:
    def __init__(self, current_edge_types, current_d_separation, index_starting_nodes, index_ending_nodes):
        self.current_edge_types = current_edge_types # assigning the current edge types
        self.current_d_separation = current_d_separation # assigning the current nodes which are part of the d-separation
        self.index_starting_nodes = index_starting_nodes # assigning the index associated with the current starting node; the starting node can be found by accesing the starting_nodes list from above, at this index
        self.index_ending_nodes = index_ending_nodes # assigning the index associated with the current ending node; the edning node can be found by accesing the edning_nodes list from above, at this index

