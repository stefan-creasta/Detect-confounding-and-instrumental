
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

    sn_list = fin.readline().split("_")
    sn = d1[sn_list[0]]
    if sn_list[1] == "i":
        sn += n

    en_list = fin.readline().split("_")
    en = d1[en_list[0]]
    if en_list[1] == "i":
        en += n
    return (d_separation, sn, en)