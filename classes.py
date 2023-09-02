# Class dedicated for storing the graph details present in the input file
class GraphDetails:
    def __init__(self, n, edge_types, map_to_id, map_to_character, d_separation, start_nodes, end_nodes):
        self.n = n # Assign the number of nodes, having ids from 0 to n - 1 - variable
        self.edge_types = edge_types # Assign the different types of edges that this graph can have - array
        self.map_to_id = map_to_id # Assign the dictionary responsible for converting chatacters to ids - dictionary (for example, node 'X' will be translated to node 0)
        self.map_to_character = map_to_character # Assign the dictionary responsible for converting ids to chatacters - dictionary (for example, node 0 will be translated to node 'X')
        self.d_separation = d_separation # Assign all of the possible nodes that can be part of set Z in a d-separation - array
        self.start_nodes = start_nodes # Assign all of the possible nodes that can be start nodes - array
        self.end_nodes = end_nodes # Assign all of the possible nodes that can be end nodes - array

# Class dedicated for storing details regarding the current graph, enabling iteration in the backtracking algorithm
class CurrentGraphDetails:
    def __init__(self, current_edge_types, current_d_separation, index_start_nodes, index_end_nodes):
        self.current_edge_types = current_edge_types # Assign the current edge types - array
        self.current_d_separation = current_d_separation # Assign the current nodes which are being conditioned on - array
        self.index_start_nodes = index_start_nodes # Assign the index associated with the current start node - variable (the starting node can be found by accesing the start_nodes list from above, at this index)
        self.index_end_nodes = index_end_nodes # Assign the index associated with the current end node - variable (the ending node can be found by accesing the end_nodes list from above, at this index)
