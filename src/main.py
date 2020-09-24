import argparse
from src.rpq import rpq
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State, Symbol, EpsilonNFA
from pyformlang.regular_expression import Regex
from pygraphblas import Matrix, BOOL, lib

from src.graph import Graph


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--graph_path'
        , required=True
        , help='path to file with graph'
    )

    parser.add_argument(
        '--regex_path'
        , required=True
        , help='path to file with regex'
    )

    parser.add_argument(
        '--out'
        , required=False
        , help='path to file with output vertices'
    )

    parser.add_argument(
        '--to'
        , required=False
        , help='path to file with input vertices'
    )

    args = parser.parse_args()
    Graph.get_answer(args)


if __name__ == '__main__':
    main()
