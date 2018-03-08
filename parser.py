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


def Parser(Tokens, ParseTable):

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
            #s.pop()              
            putContents(matched, getStack(s), Tokens[i:len(Tokens)], action, j, moves)
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
            putContents(matched, getStack(s), Tokens[i:len(Tokens)], action, j, moves)
            j = j + 1
        
        s.pop()
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

Parser(Tokens, ParseTable)

#print(ParseTable)
