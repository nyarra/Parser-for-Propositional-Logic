import string
import re
UPPER_CASE = set(string.ascii_uppercase)

class Location:
    def __init__(self, line, col):
        self.col = col
        self.line = line


class TokenKind:
    ID = 0   # identifier
    LPAR = 1 # (
    RPAR = 2 # )
    NOT = 3  # !
    AND = 4  # /\
    OR = 5   # \/
    IMPLIES = 6  # =>
    IFF = 7  # <=>
    COMMA = 8 # ,



class Token:
    def __init__(self, loc, kind):
        self.loc = loc
        self.kind = kind

    def __str__(self):
        return str(self.kind)


class Lexer:
    def __init__(self, text, lineNumber):
        self.filename = text
        self.line = lineNumber



    def tokenize(self):
        current_match = None

        #the following assignment and if statement are only to allow the test pass. they need to be removed
        line_col = []
        final_return = []

        # regex - ( ----- \(
        # regex - ) ----- \)
        # regex - \/ ---- \\/
        # regex - /\ ---- /\
        # regex - <=> ---- <=>
        # regex - ID ---- \w
        # regex - , ---- ,
        regex_list = ['[A-Za-z0-9]', '\(', '\\)', '!', '(/\\\)', '\\\/', '(?<!<)=>', '<=>', ',']
        #regex_list = ["[A-Za-z0-9]",'\\(', '\\)', '!', "r'/\\'", '\\/', '(?<!<)=>', '<=>', ',']

        data_line = ''.join(self.filename.split(' '))
        for y in regex_list:
            locations = [z.start() for z in re.finditer(y, data_line)]
            if len(locations) > 0:
                for a in locations:
                    line_col.append([self.line, a + 1, regex_list.index(str(y))])

        s_line_col = sorted(line_col, key=lambda x: (x[0], x[1]))
        for i in s_line_col:
            final_return.append(Token(Location(i[0],i[1]),i[2]))
        return final_return
