from antlr4 import *
from antlr4.error.Errors import ParseCancellationException
from antlr4.tree.Tree import TerminalNodeImpl

from src.antlr.grammar_dbLexer import grammar_dbLexer
from src.antlr.grammar_dbListener import grammar_dbListener
from src.antlr.grammar_dbParser import grammar_dbParser
from graphviz import Digraph


def get_node_name(ctx: ParserRuleContext):
    if isinstance(ctx, TerminalNodeImpl):
        return ctx.symbol.text
    else:
        return str(type(ctx).__name__).replace('Context', '').lower()


class Traverser(grammar_dbListener):
    def __init__(self, img: Digraph):
        self.img = img
        self.counter = 0
        self.node_to_id = dict()

    def enterEveryRule(self, ctx: ParserRuleContext):
        if ctx not in self.node_to_id:
            self.img.node(self.get_node_id(ctx), label=get_node_name(ctx))
        for child in ctx.children:
            self.img.node(self.get_node_id(child), label=get_node_name(child))
            self.img.edge(self.get_node_id(ctx), self.get_node_id(child))

    def get_node_id(self, node: ParserRuleContext):
        if node not in self.node_to_id:
            self.node_to_id[node] = self.counter
            self.counter += 1
        return str(self.node_to_id[node])


class Helper:
    def __init__(self, input_stream: InputStream):
        lexer = grammar_dbLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = grammar_dbParser(stream)
        parser.removeErrorListeners()
        try:
            self.tree = parser.script()
        except ParseCancellationException:
            self.tree = None

    def get_image(self, output_file):
        img = Digraph()
        if self.tree is not None:
            ParseTreeWalker().walk(Traverser(img), self.tree)
            img.render(output_file)
        else:
            raise ParseCancellationException
