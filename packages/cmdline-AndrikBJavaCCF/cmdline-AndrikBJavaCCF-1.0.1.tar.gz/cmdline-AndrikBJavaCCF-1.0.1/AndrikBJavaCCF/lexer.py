def tokenize_file(file_name):
    file = open(file_name, encoding='utf-8')
    return Lexer(file.read()).tokenize_text()


class TokenType:
    (whitespace,
     comment,
     annotation,
     keyword,
     separator,
     operator,
     identifier,
     number_literal,
     string_literal,
     error,
     *_) = range(20)


class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column


class Token:
    def __init__(self, token_type, value, position=None):
        self.token_type = token_type
        self.value = value
        self.position = position
        self.second_value = value

    def __repr__(self):

        if self.token_type == TokenType.whitespace:
            string = f'{self.token_type}: {ord(self.value)}'
        else:
            string = f'{self.token_type}, {self.value} -> {self.second_value}'

        if self.position is not None:
            string += f'\tposition: {self.position.row}:{self.position.column}'

        return string

    def __str__(self):
        return repr(self)


class Lexer:
    keywords = ("abstract", "assert", "null",
                "boolean", "break", "byte", "case", "catch", "char", "class", "const", "continue",
                "default", "do", "double", "else", "enum", "extends", "final", "finally", "float", "for",
                "if", "goto", "implements", "import", "instanceof", "int", "interface", "long",
                "native", "new", "package", "private", "protected", "public", "return",
                "short", "static", "strictfp", "super", "switch", "synchronized",
                "this", "throw", "throws", "transient", "try", "void", "volatile", "while")

    def __init__(self, text):
        self.text = text
        self.len = len(text)
        #
        self.curr_line = 1
        self.curr_pos_in_line = 1  # start of token
        self.i = 0
        self.j = 0  # end of curr token
        self.tokens = []

    def add_token(self, token_type, value):
        self.tokens.append(Token(token_type, value, Position(self.curr_line, self.curr_pos_in_line)))

    def tokenize_text(self):
        while self.i < self.len:
            c = self.text[self.i]

            if c.isspace():
                self.add_space(c)
                continue

            start_symbols = c

            if self.i + 1 < self.len:
                start_symbols = c + self.text[self.i + 1]

            # comments
            if start_symbols == "//":
                self.add_single_line_comment()
                continue
            elif start_symbols == "/*":
                self.add_multi_line_comment()
                continue

            if c in ('\'', '"'):
                token_type = TokenType.string_literal
                self.read_string(c)

            elif c.isdigit():
                token_type = TokenType.number_literal
                self.read_num_or_ident()

            elif c.isalpha() or c == '_':
                token_type = TokenType.identifier
                self.read_num_or_ident()
                if self.text[self.i: self.j] in self.keywords:
                    token_type = TokenType.keyword

            elif c == '@':
                token_type = TokenType.annotation
                self.read_num_or_ident()

            elif self.is_operator():
                token_type = TokenType.operator

            elif self.is_separator(c):
                token_type = TokenType.separator

            else:
                print(f'error in {self.i}, symbol: {self.text[self.i]}')
                self.i += 1
                continue

            self.add_token(token_type, self.text[self.i: self.j])
            self.curr_pos_in_line += self.j - self.i
            self.i = self.j

        return self.tokens

    def add_space(self, c):
        self.add_token(TokenType.whitespace, c)
        self.i += 1
        if c == '\n':
            self.curr_line += 1
            self.curr_pos_in_line = 1
        elif c == ' ':
            self.curr_pos_in_line += 1
        elif c == '\t':
            self.curr_pos_in_line += 4 - ((self.curr_pos_in_line - 1) % 4)

    def add_single_line_comment(self):
        i = self.text.find('\n', self.i + 2)
        if i == -1:
            i = self.len

        comment = self.text[self.i: i]
        self.add_token(TokenType.comment, comment)

        # we dont need to change current pos in line
        self.i = i  # because /n will be added in next iter

    def add_multi_line_comment(self):
        i = self.text.find('*/', self.i + 2)
        if i != -1:
            i += 2
        else:  # not ended comment
            comment = self.text[self.i: self.len]
            self.add_token(TokenType.comment, comment)
            self.i = self.len
            return

        comment = self.text[self.i: i]
        self.add_token(TokenType.comment, comment)

        start_of_line = self.text.rfind('\n', self.i, i)
        if start_of_line != -1:
            self.curr_line += self.text.count('\n', self.i, i)  # at less one
            self.curr_pos_in_line = i - start_of_line

        self.i = i

    def read_string(self, esc_symbol):
        self.j = self.i + 1
        while self.j < self.len:
            if self.text[self.j] == esc_symbol:
                self.j += 1
                return
            if self.text[self.j] == '\\':
                self.j += 1
            self.j += 1

    def read_num_or_ident(self):
        self.j = self.i + 1

        def is_part_of_ident(c):
            return c.isdigit() or c.isalpha() or c == '_'

        while self.j < self.len:
            if not is_part_of_ident(self.text[self.j]):
                return
            self.j += 1

    # set j if token is operator
    def is_operator(self):
        operators = ('>>>=', '>>=', '<<=', '%=', '^=', '|=', '&=', '/=',
                     '*=', '-=', '+=', '<<', '--', '++', '||', '&&', '!=',
                     '>=', '<=', '==', '%', '^', '|', '&', '/', '*', '-',
                     '+', ':', '?', '~', '!', '<', '>', '=', '...', '->', '::')
        for j in range(4, 0, -1):
            if self.i + j > self.len:
                continue
            if self.text[self.i:self.i + j] in operators:
                self.j = self.i + j
                return True

    def is_separator(self, c):
        separators = ('(', ')', '{', '}', '[', ']', ';', ',', '.')
        if c in separators:
            self.j = self.i + 1
            return True