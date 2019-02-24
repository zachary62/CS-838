import re
import ml

# candidate of all sub strings
class candidate:
    def __init__(self, position,feature1,feature2):
        # position is a array of int
        # for example "Elon Musk" in "Elon Musk has three wives" will have position [0,1]
        # for example "wives" in "Elon Musk has three wives" will have position [4]
        self.position = position

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
  for i in range(1, 59):
    file = str(i).zfill(3)
    f = open("../I/" + file + "l.txt", "r", encoding='utf-8-sig')

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

    texts.append(text)
    labels.append(label)

  return texts,labels

# TODO: return all candidates of given text
# for example, "Elon Musk has three wives"
# return features of  "Elon, Musk, has, three, wives,
# Elon Musk, Musk has, has three, three wives,
# Elon Musk has, Musk has three, has three wives"
def generatecandiates(texts):
  candidates = []
  candidates.append(candidate([0],1,1))
  candidates.append(candidate([0],1,1))
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
  # print(texts)
  # print(labels)
  candidates = generatecandiates(texts)
  candidates = preprocess(candidates)
  candidates = ml.traindata(candidates,labels)
  candidates = postprocess(candidates)
  evaluate(candidates)


if __name__== "__main__":
  main()
