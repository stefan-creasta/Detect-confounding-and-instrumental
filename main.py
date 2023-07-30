import numpy as np
import sys
from graph_constructor import read_graph, construct_graph, Node, Edge
from graph_algorithms import is_grand_child, find_cycle, cannot_get_to
from d_separation import read_d_separation_and_start_end, printing
from backtracking import backtracking
from instrumental_node import read_instrumental_info
from classes import GraphDetails, CurrentGraphDetails

fin = open("multiple_confoundings.txt", "r")
fout = open("output.txt", "w")

(n, edges, d1, revD1) = read_graph(fin)

(d_separation, sn, en) = read_d_separation_and_start_end(fin, n, d1)

graph_details = GraphDetails(n, edges, d1, revD1, d_separation, sn, en)

current_graph_details = CurrentGraphDetails(np.zeros(len(edges)), np.zeros(len(d_separation)), 0, 0)

instrumental = read_instrumental_info(fin, d1)
printing(revD1, sn[0], n, fout)
printing(revD1, en[0], n, fout)
fout.write("\n")
#fout.write(revD1[sn[0]] + " " + revD1[en[0]] + "\n")

limit_solutions = False
sys.setrecursionlimit(10000000)
backtracking(instrumental, graph_details, current_graph_details, fout, limit_solutions, 1)