from lexer import Lexer, TokenKind

from parser1 import Parser, NotImplementedError1
filepath = 'input.txt'


class Test():
    def test1(self):
        file = open(filepath, 'r')
        data = file.readlines()
        line_number = 0

        for lines in range(len(data)):
            try:
                line_number = line_number + 1
                l = Lexer(data[lines], line_number).tokenize()
                Parser().parse(l)
            except NotImplementedError1:
                pass


if __name__ == '__main__':
    test_object = Test()
    test_object.test1()
