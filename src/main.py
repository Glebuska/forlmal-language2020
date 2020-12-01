import argparse
import time
from pyformlang.regular_expression import Regex
from pygraphblas import *

from src.graph import Graph
from src.query_language import run_script


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


if __name__ == '__main__':
    main()
