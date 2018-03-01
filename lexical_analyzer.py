from collections import defaultdict
import re
k = 1

with open('input.txt') as f:
    array = f.readlines()

array = [x.strip() for x in array]
array = [x.split(" ") for x in array]
#array = []

#for i in range(T):
#    array.append(f.readline().strip().split(' '))

f.close()

print(array)
#token_dict
tokens = defaultdict(list)
keywords = ['__LINE__', '__ENCODING__', '__FILE__', 'BEGIN', 'END', 'alias',
'and', 'begin', 'break', 'case', 'class', 'def', 'defined?', 'do', 'else',
'elsif', 'end', 'ensure', 'for', 'false', 'if', 'in', 'module', 'next', 'nil',
'not', 'or', 'redo', 'rescue', 'retry', 'return', 'self', 'super', 'then', 'true'
, 'undef', 'unless', 'until', 'when', 'while', 'yield']

punctuators = ['[', ']', '(', ')', '{', '}', '::', ',', ';', '..', '...', '?',
':', '=>']

operators = ['!', '!=', '!-', '&&', '||', '=', '^', '&', '|', '<=>', '==', '==='
, '=-', '>', '>=', '<', '<=', '<<', '>>', '+', '-', '*', '/', '%', '**', '+@',
'-@', '[]', '[]=', '\'', '\"']

for word in array:
   for words in word:
      if words in keywords:
          tokens["Keyword"].append(words)
      elif words in punctuators:
          tokens["Punctuator"].append(words)
      elif words in operators:
          tokens["Operator"].append(words)
      elif re.search(r"^[+-]?(0|[1-9](_?[0-9])*)$", words) or re.search(r"^()[+|-]?0(d|D)[0-9](_?[0-9])*$", words) or re.search(r"^0[bB][01](_?[0|1])*$", words):
          tokens["Literal"].append(words)
      elif re.search(r"^0(_|o|O)?[0-7](_?[0-7])*$", words) or re.search(r"^0(x|X)[0-9a-fA-F](_?[0-9a-fA-F])*$", words) or re.search(r"^[+-]?([0-9](_?[0-9])*)?\.\d+(_?[0-9])*$", words):
      #re.search(r"^[+-]?\d+(?:\.\d+)$", words):
          tokens["Literal"].append(words)
      elif re.search(r"^(?![0-9]).+$", words):
          if re.search(r"^((\$|\@|@@)[0-9]*)?[a-zA-Z_]+[a-zA-Z0-9_]*$", words) or re.search(r"^[a-zA-Z_]+[a-zA-Z0-9]*(!|\?|=)$", words) or (r"^[A-Z]+[a-zA-Z0-9_]*$", words):
              tokens["Identifier"].append(words)
      elif re.search(r"^[+-]?([0-9](_?[0-9])*)\.\d+((_?[0-9])*|(0|[1-9](_?[0-9])*))[eE][+-]?[0-9](_?[0-9])*$", words):
          tokens["Literal"].append(words)
      elif re.search(r"^\'(\\|\')*\'$", words) or re.search(r"^$", words):
          tokens["Literal"].append(words)
      else:
          print(words, ": Invalid token")
          k = 0
          break

if k != 0:
   print(tokens)

for key, value in tokens.items():
    for v in value:
        if v == 'for':
            print(key)
