from pyformlang.cfg import CFG
from pygraphblas import *
from pyformlang.regular_expression import Regex

from src.rpq import rpq


class Graph:
    def __init__(self):
        self.size = 0
        self.matrices = dict()
        self.start_states = list()
        self.final_states = list()

    def get_intersection(self, r):
        result = Graph()

        for label in self.matrices:
            if label in r.matrices:
                result.matrices[label] = \
                    self.matrices[label].kron(r.matrices[label])

        result.size = self.size * r.size
        for i in self.start_states:
            for j in r.start_states:
                result.start_states.append(i * self.size + j)
        for i in self.final_states:
            for j in r.final_states:
                result.final_states.append(i * self.size + j)

        # get answer
        for label in result.matrices:
            print(f'Label: {label}, count: {result.matrices[label].nvals}')
        print()
        return result

    @staticmethod
    def get_closure(graph):
        closure_matrix = Matrix.sparse(BOOL, graph.size, graph.size)
        for label in graph.matrices:
            if graph.matrices[label].nrows < graph.size:
                graph.matrices[label].resize(graph.size, graph.size)
            closure_matrix = closure_matrix + graph.matrices[label]

        tmp = closure_matrix.dup()
        closure_matrix += closure_matrix @ closure_matrix
        while not tmp.iseq(closure_matrix):
            tmp = closure_matrix
            closure_matrix += closure_matrix @ closure_matrix

        return closure_matrix

    @staticmethod
    def get_answer(args):
        graph: Graph = Graph()
        graph.build_graph(args.graph_path)

        regex: Graph = Graph()
        regex.build_regex(args.regex_path)

        intersection, res = rpq(graph, regex)

        out = None
        if args.out is not None:
            with open(args.out, 'r') as f:
                out = list(map(int, f.readline().split()))

        to = None
        if args.to is not None:
            with open(args.to, 'r') as f:
                to = list(map(int, f.readline().split()))

        ans = list()

        for i, j, _ in zip(*res.select(lib.GxB_NONZERO).to_lists()):
            if (out is None) or (i in out):
                if (to is None) or (j in to):
                    ans.append((i, j))

        ans.sort()
        print(ans)
        return intersection, ans

    def build_graph(self, path):
        with open(path, 'r') as file:
            for line in file:
                (out, label, to) = line.split()
                out, to = int(out), int(to)

                if max(out, to) + 1 > self.size:
                    self.size = max(out, to) + 1
                size = self.size

                if label in self.matrices:
                    self.matrices[label].resize(size, size)
                    self.matrices[label][out, to] = 1
                else:
                    boolean_matrix = Matrix.sparse(BOOL, size, size)
                    boolean_matrix[out, to] = 1
                    self.matrices[label] = boolean_matrix

        for v in range(self.size):
            self.start_states.append(v)
            self.final_states.append(v)

    def build_regex(self, path):
        with open(path, 'r') as regex_file:
            regex_line = regex_file.read()

        dfa = Regex \
            .from_python_regex(regex_line) \
            .to_epsilon_nfa() \
            .to_deterministic() \
            .minimize()

        states = {}
        count = 0
        for state in dfa._states:
            if state not in states:
                states[state] = count
                count = count + 1
        self.size = count

        for state in dfa._states:
            for label in dfa._input_symbols:
                edges = dfa._transition_function(state, label)
                for j in edges:
                    if label in self.matrices:
                        self.matrices[label][states[state], states[j]] = 1
                    else:
                        # create new matrix for out label
                        tmp = Matrix.sparse(BOOL, self.size, self.size)
                        tmp[states[state], states[j]] = 1
                        self.matrices[label] = tmp
        self.start_states.append(states[dfa.start_state])

        for state in dfa._final_states:
            self.final_states.append(states[state])

    @staticmethod
    def build_grammar(path):
        prod = list()
        with open(path, 'r') as file:
            for line in file:
                split_line = line.split()
                cur_prod = split_line[0] + ' -> ' + ' '.join(split_line[1:])
                prod.append(cur_prod)

        prod = '\n'.join(prod)
        return CFG.from_text(prod)
