from src.graph import Graph
from src.cyk import cyk

def run_script(script, path):
    graph = Graph()
    grammar = graph.build_grammar(path)
    # script_prepared = prepare_script(script)
    script_prepared = script
    return cyk(grammar, script_prepared)
