from pyformlang.cfg import Terminal


def cyk(grammar, word):
    size = len(word)
    if size == 0:
        return grammar.generate_epsilon()

    cfg = grammar.to_normal_form()
    result = [[set() for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for production in cfg.productions:
            if production.body == [Terminal(word[i])]:
                result[i][i].add(production.head)

    for i in range(size):
        for j in range(size - i):
            for k in range(i):
                first, second = result[j][j + k], result[j + k + 1][j + i]
                for production in cfg.productions:
                    if (len(production.body) == 2
                            and production.body[0] in first
                            and production.body[1] in second):
                        result[j][j + i].add(production.head)

    return cfg.start_symbol in result[0][size - 1]
