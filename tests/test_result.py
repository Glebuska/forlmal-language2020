import argparse

from src.graph import Graph
from src.hellings import hellings
from src.cyk import cyk
from src.cfpq import cfpq_tensor_product, cfpq_matrix_product


def test_graph_0():
    args = argparse.Namespace(graph_path="tests/data/graph0.txt", out=None
                              , regex_path="tests/data/query0.txt", to=None)
    graph, res = Graph.get_answer(args)
    assert graph.matrices['a'].nvals == 6
    assert graph.matrices['b'].nvals == 1
    assert res == [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (3, 0)]


def test_graph_0_out():
    args = argparse.Namespace(graph_path="tests/data/graph0.txt", out="tests/data/out0.txt"
                              , regex_path="tests/data/query0.txt", to=None)
    graph, res = Graph.get_answer(args)
    assert graph.matrices['a'].nvals == 6
    assert graph.matrices['b'].nvals == 1
    assert res == [(1, 2), (1, 3)]


def test_graph_0_to():
    args = argparse.Namespace(graph_path="tests/data/graph0.txt", out=None
                              , regex_path="tests/data/query0.txt", to="tests/data/to0.txt")
    graph, res = Graph.get_answer(args)
    assert graph.matrices['a'].nvals == 6
    assert graph.matrices['b'].nvals == 1
    assert res == [(0, 3), (1, 3), (2, 3)]


def test_graph_0_out_to():
    args = argparse.Namespace(graph_path="tests/data/graph0.txt", out="tests/data/out0.txt"
                              , regex_path="tests/data/query0.txt", to="tests/data/to0.txt")
    graph, res = Graph.get_answer(args)
    assert graph.matrices['a'].nvals == 6
    assert graph.matrices['b'].nvals == 1
    assert res == [(1, 3)]


def test_graph_1():
    args = argparse.Namespace(graph_path="tests/data/graph1.txt", out=None
                              , regex_path="tests/data/query1.txt", to=None)
    graph, res = Graph.get_answer(args)
    assert graph.matrices['a'].nvals == 2
    assert graph.matrices['b'].nvals == 2
    assert graph.matrices['c'].nvals == 1
    assert res == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]


def test_cyk_1():
    grammar = Graph.build_grammar('tests/data/cyk_grammar1.txt')
    assert cyk(grammar, '')
    assert cyk(grammar, 'ab')
    assert cyk(grammar, 'abab')
    assert cyk(grammar, 'ababab')
    assert cyk(grammar, 'aabb')
    assert not cyk(grammar, 'a')
    assert not cyk(grammar, 'b')
    assert not cyk(grammar, 'abb')


def test_cyk_2():
    # palindrome
    grammar = Graph.build_grammar('tests/data/cyk_grammar2.txt')
    assert cyk(grammar, '')
    assert cyk(grammar, 'a')
    assert cyk(grammar, 'b')
    assert cyk(grammar, 'aba')
    assert cyk(grammar, 'bbbbb')
    assert not cyk(grammar, 'abbbab')


def test_hellings_1():
    grammar = Graph.build_grammar("tests/data/hellings_grammar.txt")
    graph = Graph()
    graph.build_graph("tests/data/hellings_graph.txt")

    assert Graph.get_closure(graph) == hellings(grammar, graph)


def test_cfpq_mul_1():
    grammar = Graph.build_grammar("tests/data/hellings_grammar.txt")
    graph = Graph()
    graph.build_graph("tests/data/hellings_graph.txt")

    assert Graph.get_closure(graph) == cfpq_matrix_product(graph, grammar) == hellings(grammar, graph)


def test_cfpq_mul_2():
    grammar = Graph.build_grammar("tests/data/cyk_grammar1.txt")
    graph = Graph()
    graph.build_graph("tests/data/graph0.txt")

    assert Graph.get_closure(graph) == cfpq_matrix_product(graph, grammar)


def test_cfpq_tensor_mul1():
    grammar = Graph.build_grammar("tests/data/cyk_grammar1.txt")
    graph = Graph()
    graph.build_graph("tests/data/graph0.txt")

    assert Graph.get_closure(graph) == cfpq_tensor_product(graph, grammar)


def test_cfpq_tensor_mul2():
    grammar = Graph.build_grammar("tests/data/hellings_grammar.txt")
    graph = Graph()
    graph.build_graph("tests/data/hellings_graph.txt")

    assert Graph.get_closure(graph) == cfpq_tensor_product(graph, grammar)
