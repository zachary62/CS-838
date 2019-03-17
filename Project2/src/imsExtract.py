import urllib.request
import sys

def process(str):
  str = str.replace("<span class=\"highlight\">", "")
  str = str.replace("</span>", "")
  if str[-2:] == " /":
    str = str[:-2]
  return str

def main():
  index = 1
  f = open("ims.csv", "w",encoding="utf-8")
  f.write("ID, name, author, year")

  for i in range(337):
    index, strr = ParseWeb("https://vufind.carli.illinois.edu/vf-ims/Search/Home?lookfor=computer+science&type=all&start_over=1&submit=Find&page="+ str(i + 1), index)
    f.write(strr)
  # print("d")

  # for i in range(75):
  #   index, strr = ParseWeb("https://www.amazon.com/s?k=programming&i=stripbooks&page="+ str(i + 1), index)
  #   f.write(strr)
  # print("d")
  # for i in range(75):
  #   index, strr = ParseWeb("https://www.amazon.com/s?k=software&i=stripbooks&page="+ str(i + 1), index)
  #   f.write(strr)
  # print("d")
  # for i in range(75):
  #   index, strr = ParseWeb("https://www.amazon.com/s?k=Operating+Systems&i=stripbooks&page="+ str(i + 1), index)
  #   f.write(strr)
  # print("d")
  # for i in range(75):
  #   index, strr = ParseWeb("https://www.amazon.com/s?k=computer+algorithm&i=stripbooks&page="+ str(i + 1) , index)
  #   f.write(strr)
  f.close()

def ParseWeb(webstr, index):
  user_agent = 'Mozilla/6.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
  headers={'User-Agent':user_agent,}
  request=urllib.request.Request(webstr,None,headers) #The assembled request
  response = urllib.request.urlopen(request)
  data = response.read() # The data u need
  mystr = data.decode("utf8")
  response.close()
  books = []
  authors = []
  years = []

  k = 0
  flag = True
  while True:
    k1 = mystr.find('class=\"title\">', k + 1, -1)
    if k1 == -1:
      break
    k = mystr.find('</a>', k1, -1)
    if k == -1:
      break
    if flag:
      books.append([k1,process(mystr[k1+len("class=\"title\">"):k].strip().replace(",", "+"))])
      flag = False
    else:
      flag = True


  k = 0
  while True:
    k1 = mystr.find(' by', k + 1, -1)
    if k1 == -1:
      break
    k = mystr.find('Published', k1 + 1, -1)
    authors.append([k1,mystr[k1+3:k].strip().replace(",", "+")])

  k = 0
  while True:
    k1 = mystr.find('Published', k + 1, -1)
    if k1 == -1:
      break
    k = mystr.find('</div>', k1 + 1, -1)
    years.append([k1,mystr[k1+len("Published"):k].strip().replace(",", "+")])

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
