class Automaton:
    def __init__(self, finite_state_machine):
        self.finite_state_machine = finite_state_machine

    def match(self, text, from_pos):
        self.finite_state_machine.reset()
        cur_pos = from_pos
        while cur_pos < len(text) and self.finite_state_machine.switch_state(text[cur_pos]) is not None:
            cur_pos += 1
        if self.finite_state_machine.can_stop():
            return from_pos, cur_pos
        else:
            return None, None
