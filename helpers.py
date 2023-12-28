class OutOfRangeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Syntax:
    def __init__(self, text: str, ending_char: str, include_ending_char=False) -> None:
        self.text = text
        self.ending_char = ending_char
        self.include_ending_char = include_ending_char

KEYWORD = Syntax( text="!!" , ending_char=":" )
SEPARATOR = Syntax( text=":" , ending_char=None )
OPEN_CURL = Syntax( text="{", ending_char=None )
CLOSE_CURL = Syntax( text="}", ending_char=None )
NEW_LN = Syntax( text='\n', ending_char=None )
OPEN_STR = Syntax( text='<<', ending_char='>>', include_ending_char=True)
FUNC_CALL = Syntax( text='!', ending_char=':' )
SPACE = Syntax( text=' ', ending_char=None )
END_LN = Syntax( text=';', ending_char=None )

TOKEN_LIST = [KEYWORD, SEPARATOR, OPEN_CURL, CLOSE_CURL, NEW_LN, OPEN_STR, FUNC_CALL, SPACE, END_LN]

def query(text: str) -> Syntax:
    match text:
        case "keyword" | "kw" | "!!": return KEYWORD
        case "separator" | "sep" | ":": return SEPARATOR
        case "open_curl" | "o_curl" | "{": return OPEN_CURL
        case "close_curl" | "c_curl" | "}": return CLOSE_CURL
        case "new_ln" | "nl" | "\n": return NEW_LN
        case "open_str" | "o_str" | "<<": return OPEN_STR
        case "func_call" | "fc" | "!": return FUNC_CALL
        case "space" | " ": return SPACE
        case "end_ln" | ";": return END_LN
        case _: return -1
