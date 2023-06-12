import numpy as np

from graph_constructor import read_graph, construct_graph, Node, Edge
from graph_algorithms import is_grand_child, find_cycle, can_get_to
from d_separation import read_d_separation_and_start_end
from backtracking import backtracking
from instrumental_node import read_instrumental_info

fin = open("input.txt", "r")
fout = open("output.txt", "w")

(n, confounding, edges, d1, revD1) = read_graph(fin)

(d_separation, sn, en) = read_d_separation_and_start_end(fin, n, d1)

instrumental = read_instrumental_info(fin, d1)

backtracking(instrumental, np.zeros(len(edges)), np.zeros(len(d_separation)), edges, sn, en, d1, revD1, d_separation, n, fout)