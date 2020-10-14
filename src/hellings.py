from collections import deque
from pyformlang.cfg import CFG, Terminal
from pygraphblas import Matrix, BOOL

from src.graph import Graph


def hellings(grammar: CFG, graph: Graph):
    if graph.size == 0:
        return False
    result = {}
    deq = deque()

    if grammar.generate_epsilon():
        matrix = Matrix.sparse(BOOL, graph.size, graph.size)

        for i in range(graph.size):
            matrix[i, i] = True
            deq.append((grammar.start_symbol, i, i))

        result[grammar.start_symbol] = matrix

    cfg = grammar.to_normal_form()

    for label, matrix in graph.matrices.items():
        for prod in cfg.productions:
            if prod.body == [Terminal(label)]:
                result[prod.head] = matrix

    for var, matrix in result.items():
        for i, j, _ in zip(*matrix.to_lists()):
            deq.append((var, i, j))

    while deq:
        tmp = list()
        var, out, to = deq.popleft()

        for key, matrix in result.items():
            for i, _ in matrix[:, out]:
                for prod in cfg.productions:
                    if (len(prod.body) == 2 and prod.body[0] == key
                            and prod.body[1] == var
                            and (prod.head
                                 not in result
                                 or result[prod.head].get(i, to) is None)):
                        deq.append((prod.head, i, to))
                        tmp.append((prod.head, i, to))

        for key, matrix in result.items():
            for new_to, _ in matrix[to, :]:
                for prod in cfg.productions:
                    if (len(prod.body) == 2 and prod.body[0] == var
                            and prod.body[1] == key
                            and (prod.head
                                 not in result
                                 or result[prod.head].get(out, new_to) is None)):
                        deq.append((prod.head, out, new_to))
                        tmp.append((prod.head, out, new_to))

        for var, out, to in tmp:
            matrix = result.get(var, Matrix.sparse(
                BOOL, graph.size, graph.size))
            matrix[out, to] = True
            result[var] = matrix

    return result.get(cfg.start_symbol, Matrix.sparse(
        BOOL, graph.size, graph.size))
