from character_reader import Reader
from helpers import *

class Lexer:
    tokens = []
    def __init__(self, reader: Reader) -> None:
        self.reader = reader
        self.position = 0
        self.consumed = 0

    @property
    def string_position(self) -> str:
        return str(self.position)
    
    def lex(self):
        if self.reader.is_eof: 
            Lexer.tokens.append({
                "type": "EOF",
                "value": "EOF",
                "position": self.string_position
            })
            return
        for token in TOKEN_LIST:
            if self.reader.contents.startswith(token.text):
                if token == -1: return f"{token.text} not found"
                if token.ending_char:
                    string_pos = "{}>{}".format( self.position, self.position + self.reader.first_instance_of(token.ending_char) + len(token.ending_char) )
                    value = self.reader.contents[:self.reader.first_instance_of(token.ending_char)]
                    consume_len = self.reader.first_instance_of(token.ending_char) + len(token.ending_char)
                else:
                    string_pos = self.string_position
                    value = token.text
                    consume_len = 1
                
                Lexer.tokens.append({
                    "type": token.text,
                    "value": value,
                    "position": string_pos
                })
                break
        else:
            if not token.include_ending_char:
                ending_pos = self.reader.first_instance_of(SEPARATOR.text)
            else:
                ending_pos = self.reader.first_instance_of(token.ending_char) + len(token.ending_char) - 1
            Lexer.tokens.append({
                "type": "name/text",
                "value": self.reader.contents[:ending_pos],
                "position": "{}>{}".format( self.position, self.position + ending_pos )
            })
            consume_len = ending_pos
        self.position += consume_len
        for _ in range(consume_len): self.reader.consume()
        self.lex()
