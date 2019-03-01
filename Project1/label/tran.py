import re

for i in range(126, 200):
  file = str(i).zfill(3)
  f = open(file + ".txt", "r", encoding='utf-8-sig')
  list = []
  for x in f:
    list.extend(re.findall(r'\S+', x))

  # print(list)
  # print(list[0][0].isupper())



  f = open(file + "n.txt", "r", encoding='utf-8-sig')
  list2 = []
  for x in f:
    list2.extend(re.findall(r'\S+', x))

  # for idx, val in enumerate(list):
  #     if str(idx) in list2:
  #        print("<name>" + str(val) + "</name>", end=' ')
  #     else:
  #        print(val, end=' ')


  with open(file + "l.txt", 'a', encoding='utf-8-sig') as out:
    for idx, val in enumerate(list):
        if str(idx) in list2:
           out.write("<name>" + str(val) + "</name>" + ' ')
        else:
           out.write(str(val) + ' ')
