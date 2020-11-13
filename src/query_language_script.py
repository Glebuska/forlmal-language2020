from src.graph import Graph
from src.cyk import cyk



def query_script(script_language, path):
    graph = Graph()
    grammar = graph.build_grammar(path)
    script_prepared = script_language
    return cyk(grammar, script_prepared)