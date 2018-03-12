import importlib
import pandas as pd
import numpy as np
from collections import defaultdict
import re

################################

#----------------------
#Grammar:   (for do while loop)
#S -> ldCR
#R -> biE
#E -> fS|tF
#C -> x
#F -> e
#----------------------

#################################

def lexer()
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
      elif re.search(r"^[+-]?(0|[1-9](_?[0-9])*)$", words) or re.search(r"^()[+|-]?0(d|D)[0-9](_?[0-9])*$", words) or re.search(r"^0[bB][01](_?[0|1])*$", words):
          token["Literal"].append(words)
      elif re.search(r"^0(_|o|O)?[0-7](_?[0-7])*$", words) or re.search(r"^0(x|X)[0-9a-fA-F](_?[0-9a-fA-F])*$", words) or re.search(r"^[+-]?([0-9](_?[0-9])*)?\.\d+(_?[0-9])*$", words):
      #re.search(r"^[+-]?\d+(?:\.\d+)$", words):
          token["Literal"].append(words)
      elif re.search(r"^(?![0-9]).+$", words):
          if re.search(r"^((\$|\@|@@)[0-9]*)?[a-zA-Z_]+[a-zA-Z0-9_]*$", words) or re.search(r"^[a-zA-Z_]+[a-zA-Z0-9]*(!|\?|=)$", words) or (r"^[A-Z]+[a-zA-Z0-9_]*$", words):
              token["Identifier"].append(words)
              if words == 'x':
                  tokens.append('x')
              else:
                  tokens.append('@')
      elif re.search(r"^[+-]?([0-9](_?[0-9])*)\.\d+((_?[0-9])*|(0|[1-9](_?[0-9])*))[eE][+-]?[0-9](_?[0-9])*$", words):
          token["Literal"].append(words)
      elif re.search(r"^\'(\\|\')*\'$", words) or re.search(r"^$", words):
          token["Literal"].append(words)
      else:
          print(words, ": Invalid token")
          k = 0
          break

if k != 0:
  # print(token)
   return tokens

#for key, value in token.items():
#    for v in value:
#        if v == 'for':
#            print(key)

###########################################

#Function to check whether the top most element of the existing stack is a terminal or not
def isTerminal(top):
    if top < 97 or top > 122:
        return false
    else:
        return true

#Function to name the headers of the final output table
def Table():
    header = ['MATCHED', 'STACK', 'INPUT', 'ACTION']
    moves = pd.DataFrame(columns = header)
    return moves

#Function to get the existing stack elements in the form of a string
def getstack(s):
    stack = ''
    k = len(s) - 1
    while (k >= 0):
        stack + s[k]
        k = k - 1

#Function to fill the final output table
def putContents(matched, stack, input_buf, action, j, moves):
    moves.iloc[j] = pd.Series({'MATCHED':matched, 'STACK':stack, 'INPUT':input_buf, 'ACTION':action})

#Function to check whether the encountered production (in the parse table) is present in the list of productions or not
def match(element, prod):
    if element in prod:
        return true
    else:
        return false

#Function to place the RHS of the production (whose LHS is a non-terminal) on the stack by replacing the corresponding 
#non-terminal (the LHS)
def replaceTop(production, s):
    s.pop()
    i = len(production)-1
    while (i >= 3):
        s.append(production[i])


def Parser(tokens, ParseTable):

    moves = Table()          # For making the output table
    prod = ['S->ldcr', 'C->x', 'R->biE', 'E->fS', 'E->tF', 'F->e']   # Listing the productions of the construct
    i = 0, j = 0, error = 0

    s = []                   # Initializing stack as a list
    s.append('~')            # Placing ~ to represent an empty stack
    a = tokens[i]            # a takes in the input characters one by one
    s.append('S')            # Appending the first non-terminal, the start symbol
    top = s[len(s)-1]        # top contains the topmost element of the stack
    action = ''              
    matched = ''
    putContents(matched, getStack(s), tokens[i:len(tokens)], action, j, moves)
    j = j + 1

    while (top != '~'):          # Continue till the stack is empty 
        if top == a:             # Comparing if the topmost element of the stack same as the encountered token character or not
            matched += top       # Matched is the string that contains the elements that have been matched upto now
            action = 'match ' + top.   # Tells what action has been taken, here matching of the terminal has been done 
            s.pop()              
            putContents(matched, getStack(s), tokens[i:len(tokens)], action, j, moves)
            j = j + 1            # increment j which keeps the counter of which row to be filled in the output table
            i = i + 1            # increment the index of the token character
            a = token[i]         # Taking the next token character
        else if isTerminal(top):      # Check if any other terminal appears on the top of the stack than the allowed terminal in the input
            print ('Parsing Error')   # If yes, then it is an error
            error = 1
            break
        else if ParseTable.iloc[top, a] == 'NaN':       # If no production corresponding to the encountered terminal and non terminal is found in the table
            print ('Parsing Error')                     # then it is an error 
            error = 1
            break
        else if match(ParseTable.iloc[top, a], prod):   # If the cuurent topmost element of the stack is a non-terminal, then replace the non-terminal by its production 
            action = 'output '+ ParseTable.iloc[top, a] # on the stack, with the new topmost element as the leftmost element of the production's RHS
            replaceTop(ParseTable.iloc[top, a], s)
            putContents(matched, getStack(s), tokens[i:len(tokens)], action, j, moves)
            j = j + 1
        
        #s.pop()
        top = s[len(s)-1]

    if error != 1:             # If no error was encountered then print the output table
        print(moves)


# Parse table
# Rows are named by non-terminals
# Columns are named by terminals
index = ['S', 'C', 'R', 'E', 'F']
columns = ['b', 'd', 'e', 'f', 'i', 'l', 't', 'x']

# Filling the appropriate cells of the parse table with appropriate productions
ParseTable = pd.DataFrame(index = index, columns = columns)
ParseTable.loc['S', 'l'] = pd.Series({'l':'S->ldcr'})
ParseTable.loc['C', 'x'] = pd.Series({'x':'C->x'})
ParseTable.loc['R', 'b'] = pd.Series({'b':'R->biE'})
ParseTable.loc['E', 'f'] = pd.Series({'f':'E->fS'})
ParseTable.loc['E', 'f'] = pd.Series({'t':'E->tF'})
ParseTable.loc['F', 'e'] = pd.Series({'e':'F->e'})

tokens = lexer()

Parser(tokens, ParseTable)

#print(ParseTable)
