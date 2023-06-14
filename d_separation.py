
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
        if sn_list[1] == "i":
            sn += n
        nodes.append(sn)
    return nodes
    
# Method to print and check whether the node is of i or j type
def printing(revD1, e, n, fout):
    if e >= n: 
        fout.write(str(revD1[e - n]) + "_i ")
    else:
        fout.write(str(revD1[e]) + "_j ")