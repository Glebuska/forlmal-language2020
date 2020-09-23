import argparse

import pytest
from pygraphblas import *

from src.graph import Graph


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
