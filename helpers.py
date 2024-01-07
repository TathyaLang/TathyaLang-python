import string


class OutOfRangeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Syntax:
    def __init__(self, text: str, ending_char: str | None = None, include_ending_char=False) -> None:
        self.text = text
        self.ending_char = ending_char
        self.include_ending_char = include_ending_char


KEYWORD = Syntax(text="!!", ending_char=":")
SEPARATOR = Syntax(text=":")
CURL = Syntax(text="{", ending_char='}', include_ending_char=True)
NEW_LN = Syntax(text='\n')
STR = Syntax(text='<<', ending_char='>>', include_ending_char=True)
FUNC_CALL = Syntax(text='!', ending_char=':')
SPACE = Syntax(text=' ')
END_LN = Syntax(text=';')
COMMA = Syntax(text=',')
INT = Syntax(text='<|', ending_char='|>', include_ending_char=True)
PAREN = Syntax(text='(', ending_char=')', include_ending_char=True)
ASSIGN = Syntax(text='=')

TOKEN_LIST = [KEYWORD, SEPARATOR, CURL, NEW_LN, STR, FUNC_CALL, SPACE, END_LN, COMMA, INT, PAREN, ASSIGN]


def query(text: str) -> Syntax:
    match text:
        case "keyword" | "kw" | "!!":
            return KEYWORD
        case "separator" | "sep" | ":":
            return SEPARATOR
        case "curl" | "curl" | "{":
            return CURL
        case "new_ln" | "nl" | "\n":
            return NEW_LN
        case "str" | "str" | "<<":
            return STR
        case "func_call" | "fc" | "!":
            return FUNC_CALL
        case "space" | " ":
            return SPACE
        case "end_ln" | ";":
            return END_LN
        case "comma" | ",":
            return COMMA
        case "int" | "int" | "<|":
            return INT
        case "paren" | "(":
            return PAREN
        case "assign" | "=":
            return ASSIGN
        case _:
            return -1


def int_check(val) -> bool:
    return all([i in string.digits for i in val])


def float_check(val) -> bool:
    return all([i in string.digits + '.' for i in val])


def fetch_ints(text: str) -> list[int]:
    parsed_ints = []
    curr_int = ''
    for char in text:
        if char in string.digits:
            curr_int += char
        else:
            if curr_int:
                parsed_ints.append(int(curr_int))
                curr_int = ''
    return parsed_ints
