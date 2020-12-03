# Generated from grammar_db.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .grammar_dbParser import grammar_dbParser
else:
    from grammar_dbParser import grammar_dbParser

# This class defines a complete listener for a parse tree produced by grammar_dbParser.
class grammar_dbListener(ParseTreeListener):

    # Enter a parse tree produced by grammar_dbParser#script.
    def enterScript(self, ctx:grammar_dbParser.ScriptContext):
        pass

    # Exit a parse tree produced by grammar_dbParser#script.
    def exitScript(self, ctx:grammar_dbParser.ScriptContext):
        pass


    # Enter a parse tree produced by grammar_dbParser#stmt.
    def enterStmt(self, ctx:grammar_dbParser.StmtContext):
        pass

    # Exit a parse tree produced by grammar_dbParser#stmt.
    def exitStmt(self, ctx:grammar_dbParser.StmtContext):
        pass


    # Enter a parse tree produced by grammar_dbParser#graph.
    def enterGraph(self, ctx:grammar_dbParser.GraphContext):
        pass

    # Exit a parse tree produced by grammar_dbParser#graph.
    def exitGraph(self, ctx:grammar_dbParser.GraphContext):
        pass


    # Enter a parse tree produced by grammar_dbParser#expr.
    def enterExpr(self, ctx:grammar_dbParser.ExprContext):
        pass

    # Exit a parse tree produced by grammar_dbParser#expr.
    def exitExpr(self, ctx:grammar_dbParser.ExprContext):
        pass


    # Enter a parse tree produced by grammar_dbParser#patterns.
    def enterPatterns(self, ctx:grammar_dbParser.PatternsContext):
        pass

    # Exit a parse tree produced by grammar_dbParser#patterns.
    def exitPatterns(self, ctx:grammar_dbParser.PatternsContext):
        pass


    # Enter a parse tree produced by grammar_dbParser#pattern.
    def enterPattern(self, ctx:grammar_dbParser.PatternContext):
        pass

    # Exit a parse tree produced by grammar_dbParser#pattern.
    def exitPattern(self, ctx:grammar_dbParser.PatternContext):
        pass


    # Enter a parse tree produced by grammar_dbParser#cond.
    def enterCond(self, ctx:grammar_dbParser.CondContext):
        pass

    # Exit a parse tree produced by grammar_dbParser#cond.
    def exitCond(self, ctx:grammar_dbParser.CondContext):
        pass


    # Enter a parse tree produced by grammar_dbParser#vertices.
    def enterVertices(self, ctx:grammar_dbParser.VerticesContext):
        pass

    # Exit a parse tree produced by grammar_dbParser#vertices.
    def exitVertices(self, ctx:grammar_dbParser.VerticesContext):
        pass


    # Enter a parse tree produced by grammar_dbParser#bool1.
    def enterBool1(self, ctx:grammar_dbParser.Bool1Context):
        pass

    # Exit a parse tree produced by grammar_dbParser#bool1.
    def exitBool1(self, ctx:grammar_dbParser.Bool1Context):
        pass



del grammar_dbParser