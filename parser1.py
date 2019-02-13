from lexer import Location, Lexer
import sys

tokens = []
locations = []
output = []
length = 0
length_no_change = 0
i = 0
class VariableType:
    PROPOSITIONS = 0
    PROPOSITION = 1
    ATOMIC = 2
    MOREPROPOSITIONS = 3
    COMPOUND = 4
    CONNECTIVE = 5


class NotImplementedError1(Exception):
    pass


class Parser:
    def __init__(self):
        self.loc = Location(0, 0)

    def parse(self, tokenList):
        global length, length_no_change
        length = len(tokenList)
        length_no_change = len(tokenList)

        for j in range(len(tokenList)):
            tokens.append(tokenList[j].kind)
            locations.append((tokenList[j].loc.line, tokenList[j].loc.col))

        self.propositions()
        output.extend(["more-propositions", "Epsilon"])
        print(output)
        del output[:]

    def match(self, a):
        global i, length
        if a == 0:
            output.append("ID")
            i = i + 1
        elif a == 1:
            output.append("LAPR")
            i = i + 1
        elif a == 2:
            output.append("RAPR")
            i = i + 1
        elif a == 3:
            output.append("NOT")
            i = i + 1
        elif a == 4:
            output.append("AND")
            i = i + 1
        elif a == 5:
            output.append("OR")
            i = i + 1
        elif a == 6:
            output.append("IMP")
            i = i + 1
        elif a == 7:
            output.append("IFF")
            i = i + 1
        elif a == 8:
            output.append("COMMA")
            i = i + 1
        else:
            print("Error at line: " + str(locations[i][0]) + " and column: " + str(locations[i][1]))
            del tokens[:]
            del locations[:]
            del output[:]
            i = 0
            length = 0
            raise NotImplementedError1
        length -= 1
        return

    def atomic(self):
        global i, length
        if tokens[i] == 0:
            output.append("Atomic")
            self.match(tokens[i])
        else:
            print("Error at line: " + str(locations[i][0]) + " and column: " + str(locations[i][1]))
            del tokens[:]
            del locations[:]
            del output[:]
            i = 0
            length = 0
            raise NotImplementedError1
        return

    def compound(self):
        global i, length
        # print("Compound")
        output.append("Compund")
        if tokens[i] == 0:
            self.atomic()
            self.connective()
            try:
                self.proposition()
            except IndexError:
                print("Syntax Error: Expected a 'proposition' at line: " + str(locations[i - 1][0]) + " after column: " + str(
                    locations[i - 1][1]))
                del tokens[:]
                del locations[:]
                del output[:]
                i = 0
                length = 0
                raise NotImplementedError1
        elif tokens[i] == 1:
            try:
                self.match(tokens[i])
                try:
                    self.proposition()
                except IndexError:
                    print("Syntax Error: Expected a 'proposition' at line :" + str(
                        locations[i - 1][0]) + " after column: " + str(
                        locations[i - 1][1]))
                    del tokens[:]
                    del locations[:]
                    del output[:]
                    i = 0
                    length = 0
                    raise NotImplementedError1

                if tokens[i] == 2:
                    self.match(tokens[i])
                else:
                    print("Error at line: " + str(locations[i][0]) + " and column: " + str(locations[i][1]))
                    del tokens[:]
                    del locations[:]
                    del output[:]
                    i = 0
                    length = 0
                    raise NotImplementedError1

            except IndexError:
                print("Syntax Error: Expected ')' at line: " + str(locations[i-1][0]) + " after column: " + str(locations[i-1][1]))
                del tokens[:]
                del locations[:]
                del output[:]
                i = 0
                length = 0
                raise NotImplementedError1
        elif tokens[i] == 3:
            self.match(tokens[i])
            self.proposition()
        else:
            print("Error at line: " + str(locations[i][0]) + " and column: " + str(locations[i][1]))
            del tokens[:]
            del locations[:]
            del output[:]
            i = 0
            length = 0
            raise NotImplementedError1
        return


    def proposition(self):
        global i,length
        # print("Proposition")
        flag = False
        if tokens[i] == 0:
            if length == 1:
                flag = True
                output.append("Proposition")
                self.atomic()
            elif tokens[i + 1] == 8 or tokens[i + 1] == 2:
                flag = True
                output.append("Proposition")
                self.atomic()
            else:
                flag = True
                output.append("Proposition")
                self.compound()
        else:
            flag = True
            output.append("proposition")
            self.compound()
        if flag == False:
            print("Error at line: " + str(locations[i][0]) + " and column: " + str(locations[i][1]))
            del tokens[:]
            del locations[:]
            del output[:]
            i = 0
            length = 0
            raise NotImplementedError1
        return

    def more_propositions(self):
        # if length == 0:
        #     output.extend(["more-proposition", "epsilon"])
        # else:
        global i, length
        if length_no_change == length:
            print("Error at line: " + str(locations[i][0]) + " and column: " + str(locations[i][1]))
            del tokens[:]
            del locations[:]
            del output[:]
            i = 0
            length = 0
            raise NotImplementedError1

        if tokens[i] == 8:
            #print(tokens[i+1])
            try:
                output.append("more-proposition")
                self.match(tokens[i])
                self.propositions()
            except IndexError:
                print("Error at line: " + str(locations[i-1][0]) + " and column: " + str(locations[i-1][1]))
                del tokens[:]
                del locations[:]
                del output[:]
                i = 0
                length = 0
                raise NotImplementedError1

        else:
            print("Error at line: " + str(locations[i][0]) + " and column: " + str(locations[i][1]))
            del tokens[:]
            del locations[:]
            del output[:]
            i = 0
            length = 0
            raise NotImplementedError1
        return

    def propositions(self):
        global i,length
        flag = False
        if tokens[i] == 8:
            flag = True
            self.more_propositions()
        else:
            flag = True
            output.append("Propositions")
            self.proposition()
        if length != 0:
            flag = True
            self.propositions()
        if flag == False:
            #print("flag rest")
            print("Error at line: " + str(locations[i][0]) + " and column: " + str(locations[i][1]))
            del tokens[:]
            del locations[:]
            del output[:]
            i = 0
            length = 0
            raise NotImplementedError1
        return

    def connective(self):
        global i, length
        if tokens[i] == 4:
            output.append("Connective")
            self.match(tokens[i])
        elif tokens[i] == 5:
            output.append("Connective")
            self.match(tokens[i])
        elif tokens[i] == 6:
            output.append("Connective")
            self.match(tokens[i])
        elif tokens[i] == 7:
            output.append("Connective")
            self.match(tokens[i])
        else:
            print("Error at line: " + str(locations[i][0]) + " and column: " + str(locations[i][1]))
            del tokens[:]
            del locations[:]
            del output[:]
            i = 0
            length = 0
            raise NotImplementedError1
        return
