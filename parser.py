import importlib
import pandas as pd
import numpy as np
import re
from collections import defaultdict

###########################################

#----------------------
#Grammar:   (for do while loop)
#S -> ldCR
#R -> biE
#E -> fS|tF
#C -> x
#F -> e
#----------------------

###########################################
#lexer

def lexer():
    k = 1

    with open('input.txt') as f:
        array = f.readlines()

        array = [x.strip() for x in array]
        array = [x.split(" ") for x in array]
#array = []

#for i in range(T):
#    array.append(f.readline().strip().split(' '))

    f.close()

#print(array)
#token_dict
    token = defaultdict(list)
    tokens = []
    keywords = ['__LINE__', '__ENCODING__', '__FILE__', 'BEGIN', 'END', 'alias',
    'and', 'begin', 'break', 'case', 'class', 'def', 'defined?', 'do', 'else',
    'elsif', 'end', 'ensure', 'for', 'false', 'if', 'in', 'module', 'next', 'nil',
    'not', 'or', 'redo', 'rescue', 'retry', 'return', 'self', 'super', 'then', 'true'
    , 'undef', 'unless', 'until', 'when', 'while', 'yield', 'loop']

    punctuators = ['[', ']', '(', ')', '{', '}', '::', ',', ';', '..', '...', '?',
    ':', '=>']

    operators = ['!', '!=', '!-', '&&', '||', '=', '^', '&', '|', '<=>', '==', '==='
    , '=-', '>', '>=', '<', '<=', '<<', '>>', '+', '-', '*', '/', '%', '**', '+@',
    '-@', '[]', '[]=', '\'', '\"']

    for word in array:
        for words in word:
            if words in keywords:
                token["Keyword"].append(words)
                if words == 'loop':
                    tokens.append('l')
                if words == 'do':
                    tokens.append('d')
                if words == 'break':
                    tokens.append('b')
                if words == 'if':
                    tokens.append('i')
                if words == 'true':
                    tokens.append('t')
                if words == 'false':
                    tokens.append('f')
                if words == 'end':
                    tokens.append('e')
            elif words in punctuators:
                token["Punctuator"].append(words)
            elif words in operators:
                token["Operator"].append(words)
                tokens.append('@')
            elif re.search(r"^[+-]?(0|[1-9](_?[0-9])*)$", words) or re.search(r"^()[+|-]?0(d|D)[0-9](_?[0-9])*$", words) or re.search(r"^0[bB][01](_?[0|1])*$", words):
                token["Literal"].append(words)
                tokens.append('@')
            elif re.search(r"^0(_|o|O)?[0-7](_?[0-7])*$", words) or re.search(r"^0(x|X)[0-9a-fA-F](_?[0-9a-fA-F])*$", words) or re.search(r"^[+-]?([0-9](_?[0-9])*)?\.\d+(_?[0-9])*$", words):
      #re.search(r"^[+-]?\d+(?:\.\d+)$", words):
                token["Literal"].append(words)
                tokens.append('@')
            elif re.search(r"^(?![0-9]).+$", words):
                if re.search(r"^((\$|\@|@@)[0-9]*)?[a-zA-Z_]+[a-zA-Z0-9_]*$", words) or re.search(r"^[a-zA-Z_]+[a-zA-Z0-9]*(!|\?|=)$", words) or (r"^[A-Z]+[a-zA-Z0-9_]*$", words):
                    token["Identifier"].append(words)
                if words == 'x':
                    tokens.append('x')
                else:
                    tokens.append('@')
            elif re.search(r"^[+-]?([0-9](_?[0-9])*)\.\d+((_?[0-9])*|(0|[1-9](_?[0-9])*))[eE][+-]?[0-9](_?[0-9])*$", words):
                token["Literal"].append(words)
                tokens.append('@')
            elif re.search(r"^\'(\\|\')*\'$", words) or re.search(r"^$", words):
                token["Literal"].append(words)
                tokens.append('@')
            else:
                print(words, ": Invalid token")
                k = 0
                break

    if k != 0:
  # print(token)
        return tokens
    else:
        return -1

#for key, value in token.items():
#    for v in value:
#        if v == 'for':
#            print(key)

###################################################

#Parser

def isTerminal(top):
    if ord(top) < 97 or ord(top) > 122:
        return False
    else:
        return True


def getStack(s):
    stack = ''
    k = len(s) - 1
    while (k >= 0):
        stack = stack + s[k]
        k = k - 1
    stack = stack[::-1]
    #print(stack)
    return stack

def putContents(matched, stack, input_buf, action, df):
    data = pd.DataFrame({'MATCHED':matched, 'STACK':stack, 'INPUT':input_buf, 'ACTION':action})
    return df.append(data)

def match(element, prod):
    if element in prod:
        return True
    else:
        return False

def replaceTop(production, s):
    s.pop()
    i = len(production)-1
    while (i >= 3):
        s.append(production[i])
        i = i - 1


def Parser(tokens, ParseTable):

    #moves = Table()
    df = pd.DataFrame()
    prod = ['S->ldCR', 'C->x', 'R->biE', 'E->fS', 'E->tF', 'F->e']
    i = 0
    error = 0
    count = 0

    s = []
    s.append('~')
    a = tokens[i]
    s.append('S')
    top = s[len(s)-1]
    action = ''
    matched = ''
    input_buf = ''
    j = i
    while j < len(tokens):
        input_buf = tokens[j] + input_buf
        j = j + 1
    #print(input_buf)
    df = putContents(matched, getStack(s), tokens[i:len(tokens)], action, df)

    while (top != '~'):
        if a == '@':
            print ('Parsing Error')
            error = 1
            break
        elif top == a:
            matched += top
            action = 'match ' + top
            s.pop()
            #print(s)
            df = putContents(matched, getStack(s), tokens[i:len(tokens)], action, df)
            if a == 'f':
                i = 0
                a = tokens[i]
                count = count + 1
            else:
                i = i + 1
                if i < len(tokens):
                    a = tokens[i]
                else:
                    break
            if count == 5:
                break
        elif isTerminal(top):
            #print(top)
            print ('Parsing Error')
            error = 1
            break
        elif ParseTable.loc[top, a] == ' ':
            print ('Parsing Error')
            #print(a)
            error = 1
            break
        elif match(ParseTable.loc[top, a], prod):
            action = 'output '+ ParseTable.loc[top, a]
            matched = ''
            replaceTop(ParseTable.loc[top, a], s)
            df = putContents(matched, getStack(s), tokens[i:len(tokens)], action, df)
        else:
            print('Parsing error')
            error = 1
            break

        top = s[len(s)-1]
        #print(top)

    if error != 1:
        print(df)



index = ['S', 'C', 'R', 'E', 'F']
columns = ['b', 'd', 'e', 'f', 'i', 'l', 't', 'x']

values = {'l':['S->ldCR', ' ', ' ', ' ', ' '], 'x':[' ', 'C->x', ' ', ' ', ' '], 'b':[' ', ' ', 'R->biE', ' ', ' '],
'f':[' ', ' ', ' ', 'E->fS', ' '], 't':[' ', ' ', ' ', 'E->tF', ' '], 'e':[' ', ' ', ' ', ' ', 'F->e']}
ParseTable = pd.DataFrame(values, index = index, columns = columns)

tokens = lexer()

if tokens != -1:
    Parser(tokens, ParseTable)
