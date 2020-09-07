from pygraphblas import Matrix, UINT8

from main import Automaton


def test_multiply():
    out = [0, 0, 1, 1]
    to = [0, 1, 1, 0]
    value = [5, 11, 9, 7]
    first = Matrix.from_lists(out, to, value)
    second = Matrix.dense(UINT8, 2, 2, 1)

    result = first @ second
    assert len(result) == 4
    assert all(x[2] == 16 for x in result)


def test_automaton():
    automation = Automaton()
    assert automation.dfa_1.accepts("bbbbabb")
    assert automation.dfa_2.accepts("aaaba")
    assert automation.dfa_final.accepts("ab")
    assert automation.dfa_final.accepts("ab")
    assert not automation.dfa_final.accepts("a")
    assert not automation.dfa_final.accepts("aba")
