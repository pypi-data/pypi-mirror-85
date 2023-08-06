class FiniteStateMachine:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.current_state = initial_state

    def switch_state(self, symbol):
        next_state = self.current_state.get_next_state_by_transition(symbol)
        if next_state is not None:
            self.current_state = next_state
        return next_state

    def can_stop(self):
        return self.current_state.is_final

    def reset(self):
        self.current_state = self.initial_state
