import argparse

from src.graph import Graph
from src.cyk import cyk


def run_script(script_language, path):
    graph = Graph()
    grammar = graph.build_grammar(path)
    script_prepared = script_language
    return cyk(grammar, script_prepared)


def script():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--script'
        , required=True
        , help='script language'
    )

    parser.add_argument(
        '--language'
        , required=True
        , help='path to language txt with syntax'
    )

    args = parser.parse_args()

    if run_script(args.script, args.language):
        print("String is accepted")
    else:
        print("String is declined")


script()
