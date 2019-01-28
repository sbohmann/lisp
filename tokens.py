from enum import Enum
from string_escaping import quote, unquote

class Token:
    def __init__(self, text, path, line, column):
        self.text = text
        self.path = path
        self.line = line
        self.column = column


class StringLiteral(Token):
    def __init__(self, text, path, line, column):
        super().__init__(text, path, line, column)
        self.value = unquote(self.text)


class IntegerLiteral(Token):
    def __init__(self, text, path, line, column):
        super().__init__(text, path, line, column)
        self.value = int(self.text)


class Bracket(Token):
    def __init__(self, text, path, line, column):
        super().__init__(text, path, line, column)
        self.set_bracket_properties()

    def set_bracket_properties(self):
        self.set_opening_and_closing_porperties()
        self.set_type_properties()

    def set_opening_and_closing_porperties(self):
        if self.text in {'(', '[', '{', }:
            self.opening = True
            self.closing = False
        elif self.text in {')', ']', '}'}:
            self.opening = False
            self.closing = True
        else:
            self.report_unsupported_bracket_format()

    def set_type_properties():
        if self.text in {'(', ')'}:
            self.type = BracketType.Parenthesis
        elif self.text in {'[', ']'}:
            self.type = BracketType.Bracket
        elif self.text in {'{', '}'}:
            self.type = BracketType.Curly
        else:
            self.report_unsupported_bracket_format()

    def report_unsupported_bracket_format():
        raise ValueError('Unsupported bracket format [' + self.text + ']')


class BracketType(Enum):
    Parenthesis = 1
    Bracket = 2
    Curly = 3
