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
   print(tokens)

#for key, value in tokens.items():
 #   for v in value:
  #      if v == 'for':
   #         print(key)
