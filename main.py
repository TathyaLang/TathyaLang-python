import character_reader, lexer, code_parser

reader = character_reader.Reader('examples/hello_world.tathya')
lexer = lexer.Lexer(reader)

lexer.lex()
print(lexer.tokens)

