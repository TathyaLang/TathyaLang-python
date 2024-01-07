from character_reader import Reader, StringReader
from helpers import *


class Lexer:
    def __init__(self, reader: Reader) -> None:
        self.reader = reader
        self.position = 0
        self.consumed = 0
        self.tokens = []
        self.lexed = False

    @property
    def string_position(self) -> str:
        return str(self.position)

    def lex(self):
        if self.reader.is_eof:
            self.tokens.append({
                "type": "EOF",
                "value": "EOF",
                "position": self.string_position
            })
            self.lexed = True
            return self
        for token in TOKEN_LIST:
            if self.reader.contents.startswith(token.text):
                print(f"Matched {token.text}")
                if token == -1: return f"{token.text!r} not found"
                if token.ending_char:
                    string_pos = "{}>{}".format(
                        self.position,
                        self.position + self.reader.first_instance_of(token.ending_char) + len(token.ending_char)
                    )
                    value = self.reader.contents[
                        :self.reader.first_instance_of(token.ending_char) +
                        (len(token.ending_char)*token.include_ending_char)
                    ]
                    consume_len = self.reader.first_instance_of(token.ending_char)
                    print(f"{string_pos=} {value=} {consume_len=} {self.reader.contents=} "
                          f"{self.reader.first_instance_of(token.ending_char)=} "
                          f"{len(token.ending_char)=} {token.include_ending_char=}")
                else:
                    string_pos = self.string_position
                    value = token.text
                    consume_len = 1

                self.tokens.append({
                    "type": token.text,
                    "value": value,
                    "position": string_pos
                })
                break
        else:
            ending_pos = self.reader.first_instance_of([SEPARATOR.text, ASSIGN.text])
            print(ending_pos, self.reader.contents)
            self.tokens.append({
                "type": "name/text",
                "value": self.reader.contents[:ending_pos],
                "position": "{}>{}".format(self.position, self.position + ending_pos)
            })
            consume_len = ending_pos
        self.position += consume_len
        for _ in range(consume_len): self.reader.consume()
        self.lex()

    def identify_curls(self) -> list[int]:
        return [i for i, token in enumerate(self.tokens) if token["type"] == '{']

    def relex(self, token_idx: int, markers: str):
        rep_token = self.tokens.pop(token_idx)
        lexed_output = Lexer(
            StringReader(rep_token["value"].strip(markers), offset=fetch_ints(rep_token["position"])[0])).lex().tokens
        for token in lexed_output[::-1]:
            self.tokens.insert(token_idx, token)
        return self

    def deep_lex(self):
        self.lex()
        curls = self.identify_curls()
        for curl in curls:
            self.relex(curl, '{}')
