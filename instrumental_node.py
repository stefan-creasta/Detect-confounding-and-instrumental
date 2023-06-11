from graph_algorithms import can_get_to

# Method to check whether a start_node is instrumental, given a graph and a final "end_node"
def is_instrumental(start_node, end_node, list, confounding, n):
    for node in list[start_node].neighbors: # we check if there is a direct edge between the start node and the end node
        if node == end_node:
            return False # if there is, we stopped, as the node is not instrumental
    # 0 means no edge, 1 means from Z to U and 2 means from U to Z
    from_Z_to_U = 0
    # 0 means no edge, 1 means from Y to U and 2 means from U to Y
    from_Y_to_U = 0
    for node in list[start_node].neighbors:
        if node == confounding:
            from_Z_to_U = 1
    for node in list[confounding].neighbors:
        if node == start_node:
            from_Z_to_U = 2
    for node in list[confounding].neighbors:
        if node == end_node:
            from_Y_to_U = 2
    for node in list[end_node].neighbors:
        if node == confounding:
            from_Y_to_U = 1
    if not (from_Y_to_U == 0 or from_Z_to_U == 0 or (from_Y_to_U == 1 and from_Z_to_U == 1)): # either there is an edge missing, either there is an immorality present
        return False
    for node in list[start_node].fathers: # check if the instrument depends only on the theta or on confounding (as well)
        if node != confounding:
            if node != start_node + 2 * n:
                return False
    can_arrive = can_get_to(start_node, end_node, list, np.zeros(3 * n), n) # the insturment is not independent of Y
    return not can_arrive
