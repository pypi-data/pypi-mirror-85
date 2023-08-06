from .patterns import *
from .automaton import *
from .finite_state_machine import *
import re


class Lexer:
    def __init__(self):
        self.tokens = []

    def tokenize(self, cpp_code):
        self.tokens.clear()
        line = cpp_code
        i = 0
        while i < len(line):
            is_matched = False
            for pattern_pair in PATTERNS:
                if isinstance(pattern_pair[0], FiniteStateMachine):
                    automaton = Automaton(pattern_pair[0])
                    match_pos = automaton.match(line, i)
                    if match_pos[0] is not None and match_pos[1] is not None:
                        matched_text = line[match_pos[0]:match_pos[1]]
                        i = match_pos[1]
                        is_matched = True
                        position = self.calculate_position(line, match_pos[0])
                        if pattern_pair[1] == TokenName.IDENTIFIER:
                            if matched_text in KEYWORDS:
                                self.tokens.append(Token(TokenName.KEYWORD, matched_text, position[0], position[1]))
                            elif matched_text in DATA_TYPES:
                                self.tokens.append(Token(TokenName.DATA_TYPE, matched_text, position[0], position[1]))
                            elif matched_text in ACCESS_MODIFIERS:
                                self.tokens.append(
                                    Token(TokenName.ACCESS_MODIFIER, matched_text, position[0], position[1]))
                            elif matched_text in PREPROCESSOR_DIRECTIVES:
                                self.tokens.append(
                                    Token(TokenName.PREPROCESSOR_DIRECTIVE, matched_text, position[0], position[1]))
                            else:
                                self.tokens.append(Token(TokenName.IDENTIFIER, matched_text, position[0], position[1]))
                        else:
                            self.tokens.append(Token(pattern_pair[1], matched_text, position[0], position[1]))
                        break
                elif isinstance(pattern_pair[0], str):
                    pattern = re.compile(pattern_pair[0], re.MULTILINE)
                    match_pos = pattern.search(line, i)
                    if match_pos is not None and match_pos.start() == i:
                        position = self.calculate_position(line, match_pos.start())
                        matched_text = line[match_pos.start():match_pos.end()]
                        is_matched = True
                        i = match_pos.end()
                        self.tokens.append(Token(pattern_pair[1], matched_text, position[0], position[1]))
                        break
            if not is_matched:
                self.tokens.append(Token(TokenName.ERROR_TOKEN, line[i]))
                i += 1

        return self.tokens


    def calculate_position(self, text, match_pos):
        num_of_new_lines = 0
        last_new_line_pos = 0
        for i in range(0, match_pos):
            if text[i] == '\n':
                num_of_new_lines += 1
                last_new_line_pos = i

        return num_of_new_lines + 1, match_pos - last_new_line_pos + 1
