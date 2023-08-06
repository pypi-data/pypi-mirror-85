from .state_machine_factory import *
from .token import *

PATTERNS = ((new_line_state_machine(), TokenName.NEW_LINE),
            (whitespace_state_machine(), TokenName.WHITESPACE),
            (r"\".*\"", TokenName.STRING),
            (r"\?", TokenName.TERNARY_OPERATOR),
            ("#", TokenName.PREPROCESSOR),
            (r"/\*([\s\S]*?)\*/\s*", TokenName.MULTILINE_COMMENT),
            (r"//.*(\r|\n|\r\n|$)", TokenName.SINGLE_LINE_COMMENT),
            (r"([0-9]*\.)[0-9]+", TokenName.FLOAT_NUMBER),
            (r"[0-9]+", TokenName.INT_NUMBER),
            (comparison_operator_state_machine(), TokenName.OPERATOR),
            (r"<<", TokenName.OPERATOR),
            (r">>", TokenName.OPERATOR),
            (operator_state_machine(), TokenName.OPERATOR),
            (separator_state_machine(), TokenName.SEPARATOR),
            (bracket_state_machine(), TokenName.BRACKET),
            (identifier_state_machine(), TokenName.IDENTIFIER),
            (char_symbol_state_machine(), TokenName.CHAR_SYMBOL))

KEYWORDS = ("for", "if", "else", "do", "while", "break", "switch", "case", "catch", "throw", "const", "continue",
            "default", "delete", "new", "asm", "enum", "explicit", "export", "enter", "true", "false", "friend",
            "goto", "inline", "namespace", "mutable", "operator", "virtual", "override", "register", "return",
            "sizeof", "static", "class", "struct", "template", "this", "try", "union", "using", "volatile", "typedef",
            "typeid", "typename", "std", "boost", "NULL")

DATA_TYPES = ("int", "float", "double", "char", "bool", "unsigned", "signed", "auto", "long", "wchar_t", "size_t",
              "void")

ACCESS_MODIFIERS = ("private", "protected", "public")

PREPROCESSOR_DIRECTIVES = ("include_next", "include", "define", "undef", "ifdef", "ifndef", "endif", "pragma")
