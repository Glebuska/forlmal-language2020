grammar grammar_db;

script : stmt* ;

stmt
    : 'connect' 'to' NAME
    | 'select' expr 'from' graph
    | 'namedPattern'  NAME pattern
    ;

graph
    : NAME
    | graph 'intersect' graph
    | 'query' pattern
    | 'start' vertices 'final' vertices 'for' graph
    ;

expr
    : 'edges'
    | 'count' 'edges'
    | 'filter' cond expr
    ;

patterns : pattern ALT pattern;
pattern
        : 'term' NAME
        | pattern 'nonterm' NAME
        | pattern STAR pattern
        | pattern PLUS pattern
        | pattern ALT pattern pattern
        | pattern patterns
        | pattern OPTION pattern
        ;

cond
    : NAME NAME NAME bool_;

vertices
    : INTS
    | 'range' 'from' NUM 'to' NUM
    | 'none'
    ;

bool_:
    |'isEquel' NAME NAME
    | 'isStart' NAME
    | 'isFinal' NAME
    | 'and' bool_ bool_
    | 'or'  bool_ bool_
    | 'not' bool_
    ;

ALT : '|' ;
OPTION : '?' ;
PLUS : '+' ;
STAR : '*' ;

NUM : '0' | [1-9] [0-9]* ;
INTS : NUM INTS;
NAME : '\''[a-z] [a-z0-9]* '\'';
WS : [ \t\r\n]+ -> skip ;