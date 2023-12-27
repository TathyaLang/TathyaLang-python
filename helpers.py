class OutOfRangeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Syntax:
    def __init__(self, text: str, ending_char: str) -> None:
        self.text = text
        self.ending_char = ending_char

KEYWORD = Syntax( text="!!" , ending_char=":" )
SEPARATOR = Syntax( text=":" , ending_char=None )
OPEN_CURL = Syntax( text="{", ending_char=None )
CLOSE_CURL = Syntax( text="}", ending_char=None )

TOKEN_LIST = [KEYWORD, SEPARATOR, OPEN_CURL, CLOSE_CURL]

def query(text: str) -> Syntax:
    match text:
        case "keyword" | "kw" | "!!": return KEYWORD
        case "separator" | "sep" | ":": return SEPARATOR
        case "open_curl" | "o_curl" | "{": return OPEN_CURL
        case "close_curl" | "c_curl" | "}": return CLOSE_CURL
        case _: return -1
