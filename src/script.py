import os
import time

from src.graph import Graph
from src.cfpq import cfpq_tensor_product, cfpq_matrix_product
from src.hellings import hellings

data = os.path.join(os.getcwd(), 'DataForFLCourse')
# tests_directory = ['WorstCase', 'FullGraph', 'MemoryAliases']
tests_directory = ['FullGraph']
times = 5

for test in tests_directory:
    path_to_test = os.path.join(data, test)

    output = open(f'{test}.csv', 'w+')

    graph_dir = os.path.join(path_to_test, 'graphs')
    for graph_name in os.listdir(graph_dir):
        graph_path = os.path.join(graph_dir, graph_name)
        graph = Graph()
        graph.build_graph(graph_path)

        grammar_dir = os.path.join(path_to_test, 'grammars')
        for grammar_name in os.listdir(grammar_dir):
            grammar_path = os.path.join(grammar_dir, grammar_name)
            grammar = Graph.build_grammar(grammar_path)
            times_list = []
            for i in range(times):
                start = time.time()
                hellings_res = hellings(grammar, graph)
                end = time.time()
                times_list.append(end - start)

            algo_time = sum(times_list) / len(times_list)

            resut_string = f'{test},{graph_name},{grammar_name},hellings,{algo_time:.3f}\r\n'
            output.write(resut_string)
            print(resut_string)

            times_list = []
            for i in range(times):
                start = time.time()
                mult_res = cfpq_matrix_product(
                    graph, grammar)
                end = time.time()
                times_list.append(end - start)

            algo_time = sum(times_list) / len(times_list)

            resut_string = f'{test},{graph_name},{grammar_name},mult,{algo_time:.3f}\r\n'
            print(resut_string)
            output.write(resut_string)

            times_list = []
            for i in range(times):
                start = time.time()
                tensor_res = cfpq_tensor_product(graph, grammar)
                end = time.time()
                times_list.append(end - start)

            algo_time = sum(times_list) / len(times_list)

            resut_string = f'{test},{graph_name},{grammar_name},tensor,{algo_time:.3f}\r\n'
            print(resut_string)
            output.write(resut_string)

            times_list = []
            for i in range(times):
                wcnf = Graph.to_wcnf(grammar)
                start = time.time()
                tensor_wcnf_res = cfpq_tensor_product(graph, wcnf)
                end = time.time()
                times_list.append(end - start)

            algo_time = sum(times_list) / len(times_list)

            resut_string = f'{test},{graph_name},{grammar_name},tensor_wcnf,{algo_time:.3f}\r\n'
            print(resut_string)
            output.write(resut_string)

    output.close()
