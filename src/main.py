import argparse
import time
from pyformlang.regular_expression import Regex
from pygraphblas import *

from src.graph import Graph
from src.query_language import run_script


def main():
    parser = argparse.ArgumentParser()

    # parser.add_argument(
    #     '--graph_path'
    #     , required=True
    #     , help='path to file with graph'
    # )
    #
    # parser.add_argument(
    #     '--regex_path'
    #     , required=True
    #     , help='path to file with regex'
    # )
    #
    # parser.add_argument(
    #     '--out'
    #     , required=False
    #     , help='path to file with output vertices'
    # )
    #
    # parser.add_argument(
    #     '--to'
    #     , required=False
    #     , help='path to file with input vertices'
    # )

    # args = parser.parse_args()
    script = "select count edges from db".replace(" ", "")
    script1 = "select edges from g1 intersect g2".replace(" ", "")
    script2 = "select edges from query * db_1".replace(" ", "")
    script3 = "select edges from query * db1".replace(" ", "")
    script4 = "connect to db1".replace(" ", "")
    script5 = "select edges from query * | query + db | query db1".replace(" ", "")
    script6 = "edges from query * | query + db | query db1".replace(" ", "")
    script7 = "select edges from * | query + db | query db1".replace(" ", "")

    if run_script(script7, "src/language.txt"):
        print("OK")

    else:
        print("Not OK")


if __name__ == '__main__':
    main()
