class State:
    def __init__(self, is_final):
        self.is_final = is_final
        self.transitions = []

    def add_transition(self, transition):
        self.transitions.append(transition)

    def get_next_state_by_transition(self, symbol):
        for transition in self.transitions:
            if transition.is_possible(symbol):
                return transition.get_state()

        return None

