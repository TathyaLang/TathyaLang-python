import character_reader, lexer, code_parser

reader = character_reader.Reader('examples/hello_world.tathya', make_logs=False)
lexer = lexer.Lexer(reader)

lexer.deep_lex()
print(*lexer.tokens, sep='\n')

