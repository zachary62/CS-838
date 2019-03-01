from colorama import init
init()
from colorama import Fore, Back, Style
import re


for i in range(126, 127):
  file = str(i).zfill(3)
  print(file)
  f = open(file + ".txt", "r", encoding='utf-8-sig')
  list = []
  for x in f:
    list.extend(re.findall(r'\S+', x))

  # print(list)
  # print(list[0][0].isupper())

  for idx, val in enumerate(list):
      if val[0].isupper() and not (val == "But" or val == "The"or val == "US"or val == "For"or val == "It"or val == "However"or val == "However,"):
        print(Fore.RED + str(idx),val, end=' ')
      else:
        print(Style.RESET_ALL+ val, end=' ')
  print()
  print()
  g = input("Enter the number of names: ")

  with open(file + "n.txt", 'a', encoding='utf-8-sig') as out:
      out.write(g)
