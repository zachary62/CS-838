import urllib.request
import sys

def main():
  index = 1
  f = open("GoodRead.csv", "w",encoding="utf-8")
  f.write("ID, name, author, year")
  for i in range(99):
    index, strr = ParseWeb("https://www.goodreads.com/search?page=" + str(i + 1) + "&q=computer+science&search_type=books&tab=books&utf8=%E2%9C%93", index)
    f.write(strr)
  for i in range(99):
    index, strr = ParseWeb("https://www.goodreads.com/search?page=" + str(i + 1) + "&q=programming&search_type=books&tab=books&utf8=%E2%9C%93", index)
    f.write(strr)
  for i in range(99):
    index, strr = ParseWeb("https://www.goodreads.com/search?page=" + str(i + 1) + "&q=software&search_type=books&tab=books&utf8=%E2%9C%93", index)
    f.write(strr)
  f.close()

def ParseWeb(webstr, index):
  fp = urllib.request.urlopen(webstr)

  mybytes = fp.read()
  mystr = mybytes.decode("utf8")
  fp.close()

  books = []
  authors = []
  years = []

  k = mystr.find('<table cellspacing')
  while True:
    k1 = mystr.find('<a title=\"', k + 1, -1)
    if k1 == -1:
      break
    k = mystr.find('\" href=', k1 + 1, -1)
    books.append([k1,mystr[k1+10:k].replace(",", "+")])


  k = mystr.find('<table cellspacing')
  while True:
    k1 = mystr.find('<span itemprop=\"name\">', k + 1, -1)
    if k1 == -1:
      break
    k = mystr.find('</span>', k1 + 1, -1)
    authors.append([k1,mystr[k1+22:k].replace(",", "+")])

  k = mystr.find('<table cellspacing')
  while True:
    k1 = mystr.find('published', k + 1, -1)
    if k1 == -1:
      break
    k = mystr.find('&mdash', k1 + 1, -1)
    years.append([k1,mystr[k1+9:k].strip().replace(",", "+")])

  curb = 0
  cura = 0
  cury = 0

  strr = ""
  while curb < len(books):
    strr = strr + "\n" + str(index) + ", " + books[curb][1] + ", "
    while cura < len(authors) and (curb == len(books) - 1  or authors[cura][0] < books[curb + 1][0]):
      strr = strr + authors[cura][1] + "; "
      cura = cura + 1
    if strr[-2:] == "; ":
      strr = strr[:-2]
    strr = strr + ", "
    if cury < len(years) and (curb == len(books) - 1  or  years[cury][0] < books[curb + 1][0]):
      strr = strr + years[cury][1]
      cury = cury + 1
    curb = curb + 1
    index = index + 1
  return index, strr

if __name__ == "__main__":
    main()
