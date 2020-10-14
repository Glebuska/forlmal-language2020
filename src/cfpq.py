from pygraphblas import Matrix, BOOL
from pyformlang.cfg import Terminal

from src.graph import Graph


def cfpq_tensor_product(graph, grammar):
    result = graph.copy()

    rfa = Graph()
    rfa_heads = dict()

    rfa.size = sum([len(production.body) + 1 for production in grammar.productions])
    index = 0
    for production in grammar.productions:
        start_state = index
        terminal_state = index + len(production.body)

        rfa.start_states.append(start_state)
        rfa.final_states.append(terminal_state)
        rfa_heads[(start_state, terminal_state)] = production.head.value

        for variable in production.body:
            matrix = rfa.matrices.get(variable.value, Matrix.sparse(BOOL, rfa.size, rfa.size))
            matrix[index, index + 1] = True
            rfa.matrices[variable.value] = matrix
            index += 1

        index += 1

    for production in grammar.productions:
        if len(production.body) == 0:
            matrix = Matrix.sparse(BOOL, graph.size, graph.size)
            matrix += Matrix.identity(BOOL, graph.size)

            result.matrices[production.head] = matrix

    is_change = True
    while is_change:
        is_change = False
        intersection = rfa.get_intersection(result)
        closure = Graph.get_closure(intersection)

        for i, j, _ in zip(*closure.to_lists()):
            rfa_from, rfa_to = i // result.size, j // result.size
            graph_from, graph_to = i % result.size, j % result.size

            if (rfa_from, rfa_to) not in rfa_heads:
                continue

            variable = rfa_heads[(rfa_from, rfa_to)]

            matrix = result.matrices.get(variable, Matrix.sparse(BOOL, graph.size, graph.size))

            if matrix.get(graph_from, graph_to) is None:
                is_change = True
                matrix[graph_from, graph_to] = True
                result.matrices[variable] = matrix

    return result.matrices.get(grammar.start_symbol, Matrix.sparse(BOOL, graph.size, graph.size))


def cfpq_matrix_product(graph, grammar):
    result = dict()

    #for filtering
    term = set()
    nonterm = set()

    if grammar.generate_epsilon():
        matrix = Matrix.sparse(BOOL, graph.size, graph.size)
        matrix += Matrix.identity(BOOL, graph.size)
        result[grammar.start_symbol] = matrix

    cfg = grammar.to_normal_form()

    for production in cfg.productions:
        if len(production.body) == 1:
            term.add(production)
        else:
            nonterm.add(production)

    for t, matrix in graph.matrices.items():
        for production in term:
            if production.body == [Terminal(t)]:
                if production.head not in result:
                    result[production.head] = matrix.dup()
                else:
                    result[production.head] += matrix.dup()

    new_changed = cfg.variables

    while len(new_changed):
        old_changed = new_changed
        new_changed = set()

        for production in nonterm:
            if production.body[0] not in result or production.body[1] not in result:
                continue

            if (production.body[0] in old_changed
                    or production.body[1] in old_changed):
                matrix = result.get(production.head, Matrix.sparse(BOOL, graph.size, graph.size))
                old_nvals = matrix.nvals
                result[production.head] = matrix + (result[production.body[0]] @ result[production.body[1]])

                if result[production.head].nvals != old_nvals:
                    new_changed.add(production.head)

    return result.get(cfg.start_symbol, Matrix.sparse(BOOL, graph.size, graph.size))
