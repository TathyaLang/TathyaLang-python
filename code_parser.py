from typing import Callable
from helpers import int_check, float_check

class Function:
    def __init__(self, name: str) -> None:
        self.name = name
        self.code: Callable = None

CO = Function('co')
def CO_code(*args: list[str], **kwargs: dict[str, str]) -> None:
    prefix = kwargs.get('p', '')
    suffix = kwargs.get('s', '')
    joiner = kwargs.get('j', ' ')

    print(prefix + joiner.join(args) + suffix)
CO.code = CO_code

CON = Function('con')
def CON_code(*args: list[str], **kwargs: dict[str, str]) -> None:
    s = kwargs.pop('s')
    CO_code(*args, s=s, **kwargs)
CON.code = CON_code

STD_FUNC_LIST = {
    'co': CO,
    'con': CON
}

class Parser:
    def __init__(self, lex_output: list[dict[str, str]]) -> None:
        self.lex_output = lex_output

        self.execution_stack: list = []
        self.variables = {}

    def parse(self, token_idx=0):
        curr_token = self.lex_output[token_idx]
        if curr_token["type"] == '!':
            func_name = curr_token["value"][1:]
            self.execution_stack.append(FunctionCall(
                func_name,
                *self.check_for_args(token_idx+4, ending=';'),
                **self.check_for_kwargs(token_idx+2)
            ))
    
    def check_for_kwargs(self, token_idx: int) -> dict:
        if self.lex_output[token_idx]["type"] == '(':
            return self.parse_kwargs(token_idx)
        return None

    def check_for_args(self, token_idx: int, ending: str) -> list:
        if (ending_idx := self.first_instance_of(token_idx, ending)) == -1: return "Syntax Error"
        return self.parse_args(token_idx, ending_idx)
    
    def first_instance_of(self, starting: int, character: str) -> int:
        for i, token in enumerate(self.lex_output[starting:]):
            if token["text"] == ';': return i + starting
        return -1

    def parse_args(self, starting_idx: int, ending_idx: int):
        args = []
        for token in self.lex_output[starting_idx:ending_idx]:
            if token["type"] == '<<': args.append(token["value"].strip("<>"))
            elif int_check(token["value"]): args.append(int(token["value"]))
            elif float_check(token["value"]): args.append(float(token["value"]))
            else: args.append(self.variables[token["value"]])
        return args
    
    def parse_kwargs(self, token_idx: int) -> dict:
        ... # TODO

class FunctionCall:
    def __init__(self, function_name: str, *args: list, **kwargs: dict) -> None:
        self.function_name = function_name
        self.args = args
        self.kwargs = kwargs
    
    def execute(self):
        return STD_FUNC_LIST[self.function_name.lower()](*self.args, **self.kwargs)
    
