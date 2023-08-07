import sys
import numpy as np
from graph_constructor import read_graph, construct_graph, Node, Edge
from graph_algorithms import is_grand_child, find_cycle, cannot_get_to
from d_separation import read_d_separation_and_start_end, printing
from backtracking import backtracking
from instrumental_node import read_instrumental_info
from classes import GraphDetails, CurrentGraphDetails

# Consider the following problem settings:
#   paper - used to reproduce the results found in the original paper
#   instrumental - used to conduct experiments on graphs with an instrument and a confounder
#   multiple_confoundings - used to conduct experiments on graphs with an instrument and two confounders

# Select the desired problem setting
problem_setting = "paper"

# Depending on the problem setting, a different input will be read
if problem_setting == "paper": # The setting proposed originally in the paper
    fin = open("paper_input.txt", "r")
elif problem_setting == "instrumental": # The setting with an instrumental variable and a single confounder
    fin = open("instrumental_input.txt", "r")
elif problem_setting == "multiple_confoundings": # The setting with an instrumental variable and two confounders
    fin = open("multiple_confoundings.txt", "r")

# Only one output file
fout = open("output.txt", "w")

# Read the present nodes and the different types of edges
(n, edges, d1, revD1) = read_graph(fin)

# Read the possible nodes that can be part of the d-separation, as well as the start and end nodes considered for the independence test
(d_separation, sn, en) = read_d_separation_and_start_end(fin, n, d1)

# Store the graph information
graph_details = GraphDetails(n, edges, d1, revD1, d_separation, sn, en)

# Initialize the necessary counters for backtracking in order to iterate over all the possible graphs, d-separations, start and end nodes
current_graph_details = CurrentGraphDetails(np.zeros(len(edges)), np.zeros(len(d_separation)), 0, 0)

# Read the info regarding the instrument: the desired instrument, the explanatory variable and the dependent variable
instrumental = read_instrumental_info(fin, d1)

# Print the first start and end nodes
printing(revD1, sn[0], n, fout)
printing(revD1, en[0], n, fout)
fout.write("\n")

# Variable for limiting the solutions or not - special variable for the input with only one confounding and insturmental, used to print only the d-separations for which the independence test differs
limit_solutions = False

# Set a very high limit for the recursion limit
sys.setrecursionlimit(10000000)

# Start the iteration through all the possible graphs, d-separations, start and end nodes
backtracking(instrumental, graph_details, current_graph_details, problem_setting, fout, limit_solutions, 1)