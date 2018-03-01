import importlib
import pandas as pd
import numpy as np
from pythonds.basic.stack import Stack

moduleName = input('lexical_analyzer.py')
importlib.import_module(moduleName)

#----------------------
#Grammar:   (for do while loop)
#S -> ldCR
#R -> biE
#E -> fS|tF
#C -> x
#F -> e
#----------------------

def isTerminal(top):
    if top < 97 or top > 122:
        return false
    else:
        return true

def Table():
    header = ['MATCHED', 'STACK', 'INPUT', 'ACTION']
    moves = pd.DataFrame(columns = header)
    return moves

def getstack(s):
    stack = ''
    k = len(s) - 1
    while (k >= 0):
        stack + s[k]
        k = k - 1

def putContents(matched, stack, input_buf, action, j, moves):
    moves.iloc[j] = pd.Series({'MATCHED':matched, 'STACK':stack, 'INPUT':input_buf, 'ACTION':action})

def match(element, prod):
    if element in prod:
        return true
    else:
        return false

def replaceTop(production, s):
    s.pop()
    i = len(production)-1
    while (i >= 3):
        s.append(production[i])


def Parser(Tokens, ParseTable):

    moves = Table()
    prod = ['S->ldcr', 'C->x', 'R->biE', 'E->fS', 'E->tF', 'F->e']
    i = 0, j = 0, error = 0

    s = []
    s.append('~')
    a = tokens[i]
    s.append('S')
    top = s[len(s)-1]
    action = ''
    matched = ''
    putContents(matched, getStack(s), tokens[i:len(tokens)], action, j, moves)
    j = j + 1

    while (top != '~'):
        if top == a: 
            matched += top
            action = 'match ' + top
            s.pop()
            putContents(matched, getStack(s), Tokens[i:len(Tokens)], action, j, moves)
            j = j + 1
            i = i + 1
        else if isTerminal(top):
            print ('Parsing Error')
            error = 1
            break
        else if ParseTable.iloc[top, a] == 'NaN':
            print ('Parsing Error')
            error = 1
            break
        else if match(ParseTable.iloc[top, a], prod):
            action = 'output '+ ParseTable.iloc[top, a]
            replaceTop(ParseTable.iloc[top, a], s)
            putContents(matched, getStack(s), Tokens[i:len(Tokens)], action, j, moves)
            j = j + 1

        s.pop()
        top = s[len(s)-1]

    if error != 1:
        print(moves)



index = ['S', 'C', 'R', 'E', 'F']
columns = ['b', 'd', 'e', 'f', 'i', 'l', 't', 'x']

ParseTable = pd.DataFrame(index = index, columns = columns)
ParseTable.loc['S', 'l'] = pd.Series({'l':'S->ldcr'})
ParseTable.loc['C', 'x'] = pd.Series({'x': 'C->x'})
ParseTable.loc['R', 'b'] = pd.Series({'b':'R->biE'})
ParseTable.loc['E', 'f'] = pd.Series({'f':'E->fS'})
ParseTable.loc['E', 'f'] = pd.Series({'t':'E->tF'})
ParseTable.loc['F', 'e'] = pd.Series({'e':'F->e'})

Parser(Tokens, ParseTable)

#print(ParseTable)
