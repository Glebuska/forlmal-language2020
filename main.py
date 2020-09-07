from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol


class Automaton:

    def __init__(self):
        self.dfa_1 = DeterministicFiniteAutomaton()
        self.dfa_2 = DeterministicFiniteAutomaton()
        self.dfa_final = DeterministicFiniteAutomaton()

        # Creation of the states
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)

        # Creation of the symbols
        symb_a = Symbol("a")
        symb_b = Symbol("b")

        # Add a start state
        self.dfa_1.add_start_state(state0)
        self.dfa_2.add_start_state(state0)
        self.dfa_2.add_start_state(state0)

        # Add two final states
        self.dfa_1.add_final_state(state1)
        self.dfa_2.add_final_state(state1)

        # Create transitions
        self.dfa_1.add_transition(state0, symb_a, state1)
        self.dfa_1.add_transition(state0, symb_b, state0)
        self.dfa_1.add_transition(state1, symb_b, state1)

        self.dfa_2.add_transition(state0, symb_b, state1)
        self.dfa_2.add_transition(state0, symb_a, state0)
        self.dfa_2.add_transition(state1, symb_a, state1)

        self.dfa_final = self.dfa_1 & self.dfa_2


# if __name__ == '__main__':
