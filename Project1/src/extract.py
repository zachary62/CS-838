import re
import ml

# candidate of all sub strings
class candidate:
    def __init__(self, text, position, feature1, feature2):
        self.text = text
        # position is a array of int
        # for example "Elon Musk" in "Elon Musk has three wives" will have position [0,1]
        # for example "wives" in "Elon Musk has three wives" will have position [4]
        self.label = position

        # TODO: define a set of features (e.g. how many substring there are, whether initial capital...)
        self.features1 = feature1
        self.features2 = feature2

# read files from I
# return text and labeled entity position
def readfile():
  # texts of all files
  texts = []
  labels = []
  # read files from I
  for i in range(1, 2):
    file = str(i).zfill(3)
    f = open("../I/" + file + "l.txt", "r", encoding='utf-8-sig')
    print("../I/" + file + "l.txt")

    # text is the sub strings of file splited by space
    # label is the position of name
    # for example, "Elon Musk has three wives"
    # text will be [Elon, Musk, has, three, wives]
    # label will be [0,1] because text[0] = Elon and text[1] = Musk are both names
    text = []
    label = []
    for x in f:
      text.extend(re.findall(r'\S+', x))

    for idx, val in enumerate(text):
      if val.startswith("<name>") and val.endswith("</name>"):
        label.append(idx)
        # delete <name> tag
        text[idx] = text[idx][6:len(text[idx])-7]
      else:
        label.append(-1) #indicates that this word is neither a name indiviually nor can it be a part of a name

    texts.append(text)
    labels.append(label)

  return texts,labels

# TODO: return all candidates of given text
# for example, "Elon Musk has three wives"
# return features of  "Elon, Musk, has, three, wives,
# Elon Musk, Musk has, has three, three wives,
# Elon Musk has, Musk has three, has three wives"
def generatecandiates(texts, labels):
  candidates = []

  #k refers to different files in I
  #generate candidates of length 1
  for k in range(0,len(texts)):
    for i in range(0,len(texts[k])):
      text = texts[k][i]
      candidates.append(candidate(text, labels[k][i], 1, 1))

  #generate candidates of length 2
  for k in range(0,len(texts)):
    for i in range(0,len(texts[k]) - 1):
      text = texts[k][i] + " " + texts[k][i+1]

      if labels[k][i] != -1 and labels[k][i+1] != -1:
        #this is a probable candidate name of length 2 words
        if texts[k][i][-1:] == ',' :
          # for strings like "Elon Musk, Mark Manson and Tom Sawyer are good friends.", candidates are generated as
          # Elon Musk, ; Musk, Mark and so on; so we need to avoid combining two names together like in Musk, Mark;
          # if a comma is encountered in probable candidate generation that indicates one name ended and another name started, then that 
          # is marked as not a name
          label = -1 
        else:
          label = labels[k][i]
      else:
        label = -1 #includes cases like "Musk has" or "said Elon" where one of the word is not a name and cases like "has three" where none of the word is a name

      candidates.append(candidate(text, label, 1, 1))

  #generate candidates of length 3
  for k in range(0,len(texts)):
    for i in range(0,len(texts[k]) - 2):
      text = texts[k][i] + " " + texts[k][i+1] + " " + texts[k][i+2]

      if labels[k][i] != -1 and labels[k][i+1] != -1 and labels[k][i+2] != -1:
        #this is a probable candidate name of length 3 words
        if texts[k][i][-1:] == ',' or texts[k][i+1][-1:] == ',':
          # for strings like "Elon Musk, Mark Manson and Tom Sawyer are good friends.", candidates are generated as
          # Elon Musk, Mark ; Musk, Mark Manson and so on; so we need to avoid combining two names together
          # if a comma is encountered in probable candidate generation that indicates one name ended and another name started, then that 
          # is marked as not a name
          label = -1 
        else:
          label = labels[k][i]
      else:
        label = -1 #includes cases like Musk has or said Elon where one of the word is not a name and cases like has three where none of the word is a name

      candidates.append(candidate(text, label, 1, 1))

  #candidates.append(candidate([0],1,1))
  #candidates.append(candidate([0],1,1))
  return candidates

# TODO: preprocess all candidates (e.g. pruning rules)
def preprocess(candidates):
  candidates = []
  candidates.append(candidate([0],1,1))
  candidates.append(candidate([0],1,1))
  return candidates

# TODO: postprocess all candidates
def postprocess(candidates):
  return 0

# TODO: evaluates result
def evaluate(candidates):
  return 0

def main():
  # read files from I
  texts,labels = readfile()
  #print(texts)
  #print(labels)
  candidates = generatecandiates(texts, labels)
  #for i in range(0,len(candidates)):
  #  print('{} {}'.format(candidates[i].text, candidates[i].label))
  candidates = preprocess(candidates)
  candidates = ml.traindata(candidates,labels)
  candidates = postprocess(candidates)
  evaluate(candidates)


if __name__== "__main__":
  main()