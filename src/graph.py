from pyformlang.cfg import CFG, Variable, Production, Terminal, Epsilon
from pygraphblas import *
from pyformlang.regular_expression import Regex

from src.rpq import rpq
from ordered_set import OrderedSet

class Graph:
    def __init__(self):
        self.size = 0
        self.matrices = dict()
        self.start_states = list()
        self.final_states = list()

    def copy(self):
        copy = Graph()

        copy.size = self.size
        copy.start_states = self.start_states
        copy.final_states = self.final_states

        for label, matrix in self.matrices.items():
            copy.matrices[label] = matrix.dup()

        return copy

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
    def to_wcnf(grammar):
        wcnf = grammar.to_normal_form()
        if grammar.generate_epsilon:
            new_start_symbol = Variable('S\'')
            new_variables = set(wcnf.variables)
            new_variables.add(new_start_symbol)
            new_productions = set(wcnf.productions)
            new_productions.add(Production(
                new_start_symbol, [wcnf.start_symbol]))
            new_productions.add(Production(new_start_symbol, []))
            return CFG(new_variables, wcnf.terminals, new_start_symbol, new_productions)
        return wcnf

    @staticmethod
    def prod_from_regex(head, regex, state_counter):
        enfa = Regex(regex).to_epsilon_nfa().minimize()
        transitions = enfa.to_dict()
        state_to_var = dict()
        production_set = OrderedSet()

        for state in enfa.states:
            state_counter[0] += 1
            state_to_var[state] = Variable(f'State{state_counter[0]}')

        for start_state in enfa.start_states:
            production_set.add(Production(head, [state_to_var[start_state]]))

        for head_state, transition in transitions.items():
            for symbol, body_state in transition.items():
                prod_head = state_to_var[head_state]
                prod_body = list()

                if symbol.value == 'eps':
                    prod_body.append(Epsilon())
                elif symbol.value.isupper():
                    prod_body.append(Variable(symbol.value))
                elif symbol.value.islower():
                    prod_body.append(Terminal(symbol.value))
                else: prod_body.append(Terminal(symbol.value))

                prod_body.append(state_to_var[body_state])
                production_set.add(Production(prod_head, prod_body))

                if body_state in enfa.final_states:
                    production_set.add(Production(
                        state_to_var[body_state], []))

        return production_set

    @staticmethod
    def build_grammar(path):
        state_counter = [0]
        with open(path, 'r') as g:
            productions = OrderedSet()

            for line in g.readlines():
                rule = line.replace('\n', '').split(' ', 1)
                var = Variable(rule[0])
                if any(symb in rule[1] for symb in '?+*|,.\'()'):
                    body = rule[1].replace('?', f'| eps')
                    productions |= Graph.prod_from_regex(var, body, state_counter)
                else:
                    body = []
                    for s in rule[1].split(' '):
                        if s == 'eps':
                            e = Epsilon()
                            body.append(e)
                        elif s.islower():
                            t = Terminal(s)
                            body.append(t)
                        elif s.isupper():
                            v = Variable(s)
                            body.append(v)
                        else:
                            t = Terminal(s)
                            body.append(t)
                    productions.add(Production(var, body))

            return CFG(start_symbol=productions[0].head, productions=productions)

