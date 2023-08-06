from .transition import *
from .state import *
from .finite_state_machine import *


def bracket_state_machine():
    initial = State(False)
    q1 = State(True)  # (
    q2 = State(True)  # )
    q3 = State(True)  # {
    q4 = State(True)  # }
    q5 = State(True)  # [
    q6 = State(True)  # ]

    initial.add_transition(SymbolTransition("(", q1))
    initial.add_transition(SymbolTransition(")", q2))
    initial.add_transition(SymbolTransition("{", q3))
    initial.add_transition(SymbolTransition("}", q4))
    initial.add_transition(SymbolTransition("[", q5))
    initial.add_transition(SymbolTransition("]", q6))
    return FiniteStateMachine(initial)


def separator_state_machine():
    initial = State(False)
    q1 = State(True)  # :
    q2 = State(True)  # ,
    q3 = State(True)  # ;
    q4 = State(True)  # ::

    initial.add_transition(SymbolTransition(":", q1))
    initial.add_transition(SymbolTransition(",", q2))
    initial.add_transition(SymbolTransition(";", q3))
    q1.add_transition(SymbolTransition(":", q4))
    return FiniteStateMachine(initial)


def whitespace_state_machine():
    initial = State(False)
    q1 = State(True)

    func_transition = lambda c: c == ' ' or c == '\t'
    q1.add_transition(FuncTransition(func_transition, q1))
    initial.add_transition(FuncTransition(func_transition, q1))
    return FiniteStateMachine(initial)


def new_line_state_machine():
    initial = State(False)
    q1 = State(True)
    transition_function = lambda c: c == '\n' or c == '\r' or c == "\r\n"
    initial.add_transition(FuncTransition(transition_function, q1))
    return FiniteStateMachine(initial)


def double_quote_string_state_machine():
    initial = State(False)
    q1 = State(False)
    q2 = State(True)
    q3 = State(False)

    str_symbols = lambda c: c != '\"' and c != '\\'
    not_slash = lambda c: c != '\\'

    q1.add_transition(FuncTransition(str_symbols, q1))
    q1.add_transition(SymbolTransition('\\', q3))
    q3.add_transition(SymbolTransition('\\', q3))
    q3.add_transition(FuncTransition(not_slash, q1))
    q1.add_transition(SymbolTransition('\"', q2))  # end string
    initial.add_transition(SymbolTransition('\"', q1))
    return FiniteStateMachine(initial)


def identifier_state_machine():
    initial = State(False)
    q1 = State(True)
    start_name_transition = lambda c: c == '_' or c.isalpha()
    initial.add_transition(FuncTransition(start_name_transition, q1))
    name_transition = lambda c: c == '_' or c.isalpha() or c.isdigit()
    q1.add_transition(FuncTransition(name_transition, q1))
    return FiniteStateMachine(initial)


def char_symbol_state_machine():
    initial = State(False)
    q1 = State(False)  # '
    q2 = State(False)  # symbol
    q3 = State(True)  # '
    initial.add_transition(SymbolTransition('\'', q1))
    q1.add_transition(FuncTransition(lambda c: c.isalpha(), q2))
    q2.add_transition(SymbolTransition('\'', q3))
    return FiniteStateMachine(initial)


def operator_state_machine():
    initial = State(False)
    q1 = State(True)  # +
    q2 = State(True)  # ++
    q3 = State(True)  # -
    q4 = State(True)  # --
    q5 = State(True)  # *
    q6 = State(True)  # /
    q7 = State(True)  # &
    q8 = State(True)  # ^
    q9 = State(True)  # |
    q10 = State(True)  # =
    q11 = State(True)  # ~
    q16 = State(True)  # %
    q17 = State(True)  # ->
    q18 = State(True)  # ->*
    q19 = State(True)  # .
    q20 = State(True)  # .*
    q21 = State(False)  # :
    q22 = State(True)  # ::

    # all to =
    q1.add_transition(SymbolTransition('=', q10))
    q3.add_transition(SymbolTransition('=', q10))
    q5.add_transition(SymbolTransition('=', q10))
    q6.add_transition(SymbolTransition('=', q10))
    q7.add_transition(SymbolTransition('=', q10))
    q8.add_transition(SymbolTransition('=', q10))
    q9.add_transition(SymbolTransition('=', q10))
    q16.add_transition(SymbolTransition('=', q10))

    q1.add_transition(SymbolTransition('+', q2))  # ++
    q3.add_transition(SymbolTransition('-', q4))  # --
    q3.add_transition(SymbolTransition('>', q17))  # ->
    q17.add_transition(SymbolTransition('*', q18))  # ->*
    q10.add_transition(SymbolTransition('*', q20))  # .*
    q21.add_transition(SymbolTransition(':', q22))  # ::

    initial.add_transition(SymbolTransition('+', q1))
    initial.add_transition(SymbolTransition('-', q3))
    initial.add_transition(SymbolTransition('*', q5))
    initial.add_transition(SymbolTransition('/', q6))
    initial.add_transition(SymbolTransition('&', q7))
    initial.add_transition(SymbolTransition('^', q8))
    initial.add_transition(SymbolTransition('|', q9))
    initial.add_transition(SymbolTransition('=', q10))
    initial.add_transition(SymbolTransition('~', q11))
    initial.add_transition(SymbolTransition('%', q16))
    initial.add_transition(SymbolTransition('.', q19))
    initial.add_transition(SymbolTransition(':', q21))

    return FiniteStateMachine(initial)


def comparison_operator_state_machine():
    initial = State(False)
    q1 = State(True)  # <
    q2 = State(True)  # >
    q3 = State(True)  # !
    q4 = State(True)  # <=, >=, !=, ==
    q5 = State(True)  # ==
    q6 = State(False)  # =

    q1.add_transition(SymbolTransition('=', q4))
    q2.add_transition(SymbolTransition('=', q4))
    q3.add_transition(SymbolTransition('=', q4))
    q6.add_transition(SymbolTransition('=', q5))

    initial.add_transition(SymbolTransition('<', q1))
    initial.add_transition(SymbolTransition('>', q2))
    initial.add_transition(SymbolTransition('!', q3))
    initial.add_transition(SymbolTransition('=', q6))

    return FiniteStateMachine(initial)
