from enum import Enum


class TokenName(Enum):
    WHITESPACE = 0  # \t, space, ......                                                                    # Done
    NEW_LINE = 1                                                                                           # Done
    OPERATOR = 2  # +, -, *, /, &, |, ^, =, +=, -=, %=, *=, /=, &=, |=, ^=, ~, <<, >>, %, ->               # Done
    COMPARISON_OPERATOR = 3  # <, <=, >, >=, ==, !=                                                        # Done
    DATA_TYPE = 4                                                                                          # Done
    KEYWORD = 5                                                                                            # Done
    SEPARATOR = 6  # , ;:                                                                                  # Done
    BRACKET = 7  # (,), [, ], {,}                                                                          # Done
    DOT = 8  # .   // Currently is an operator                                                             # Done
    IDENTIFIER = 9                                                                                         # Done
    INT_NUMBER = 10                                                                                        # Done
    STRING = 11                                                                                            # Done
    MULTILINE_STRING = 12
    ERROR_TOKEN = 13                                                                                       # Done
    TERNARY_OPERATOR = 14  # ?                                                                             # Done
    SINGLE_LINE_COMMENT = 15  # //                                                                         # Done
    CHAR_SYMBOL = 16                                                                                       # Done
    FLOAT_NUMBER = 17                                                                                      # Done
    ACCESS_MODIFIER = 18                                                                                   # Done
    MULTILINE_COMMENT = 19                                                                                 # Done
    PREPROCESSOR = 20  # #                                                                                 # Done
    PREPROCESSOR_DIRECTIVE = 21                                                                            # Done


class Token:
    def __init__(self, token_name, value=None, line=0, column=0):
        self.token_name = token_name
        self.value = value
        self.line = line
        self.column = column

    def to_string(self):
        if self.value is not None:
            return "{" + self.token_name.name + " | " + self.value + "} line " + str(self.line) + ", column " + str(self.column)
