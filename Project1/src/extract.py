import re
import ml

# candidate of all sub strings
class candidate:
    def __init__(self, text, position, label, feature1, feature2):
        self.text = text
        # position is a tuple of length 3 whose first element tells the file number in which the candidate is present
        # second element tells the location of first word of the candidate and third element tells the no of words in the candidate
        # for example "Elon Musk" in "Elon Musk has three wives" will have position [1,0,2]
        # for example "wives" in "Elon Musk has three wives" will have position [1,4,1]
        self.position = position
        # label is 1 if self.text is a valid name else it is -1
        # for example "Elon Musk" in "Elon Musk has three wives" will have label 1
        # for example "wives" in "Elon Musk has three wives" will have label -1
        self.label = label

        # TODO: define a set of features (e.g. how many substring there are, whether initial capital...)
        self.features1 = feature1
        self.features2 = feature2

# read files from I
# return text and labeled entity position
def readfile():
  # texts of all files
  texts = []
  labels = []
  positions = []
  # read files from I
  for i in range(1, 60):
    file = str(i).zfill(3)
    f = open("../I/" + file + "l.txt", "r", encoding='utf-8-sig')
    print("../I/" + file + "l.txt")

    # text is the sub strings of file splited by space
    # label is the position of name
    # for example, "Elon Musk has three wives"
    # text will be [Elon, Musk, has, three, wives]
    # label will be [1,1,-1,-1,-1] because text[0] = Elon and text[1] = Musk are both names
    # position will be [0,1,2,3,4] 
    text = []
    label = []
    position = []
    for x in f:
      text.extend(re.findall(r'\S+', x))

    for idx, val in enumerate(text):
      position.append(idx)
      if val.startswith("<name>") and val.endswith("</name>"):
        label.append(1)
        # delete <name> tag
        text[idx] = text[idx][6:len(text[idx])-7]
      else:
        label.append(-1) #indicates that this word is neither a name indiviually nor can it be a part of a name

    texts.append(text)
    labels.append(label)
    positions.append(position)

  return texts,labels,positions

# return all candidates of given text
# for example, "Elon Musk has three wives"
# return features of  "Elon, Musk, has, three, wives,
# Elon Musk, Musk has, has three, three wives,
# Elon Musk has, Musk has three, has three wives"
def generatecandiates(texts, labels, positions):
  candidates = []

  #k refers to different files in I
  #generate candidates of length 1
  for k in range(0,len(texts)):
    for i in range(0,len(texts[k])):
      pos = []
      pos.append(k+1)
      pos.append(positions[k][i])
      pos.append(1)
      text = texts[k][i]
      candidates.append(candidate(text, pos, labels[k][i], 1, 1))

  #generate candidates of length 2
  for k in range(0,len(texts)):
    for i in range(0,len(texts[k]) - 1):
      text = texts[k][i] + " " + texts[k][i+1]
      pos = []
      pos.append(k+1)
      pos.append(positions[k][i])
      pos.append(2)

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

      candidates.append(candidate(text, pos, label, 1, 1))

  #generate candidates of length 3
  for k in range(0,len(texts)):
    for i in range(0,len(texts[k]) - 2):
      text = texts[k][i] + " " + texts[k][i+1] + " " + texts[k][i+2]
      pos = []
      pos.append(k+1)
      pos.append(positions[k][i])
      pos.append(3)

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
        # includes cases like 'Musk has three' or 'said Elon Musk' where one of the word is not a name 
        # and cases like 'has three wives' where none of the word is a name
        label = -1 

      candidates.append(candidate(text, pos, label, 1, 1))

  #candidates.append(candidate([0],1,1))
  #candidates.append(candidate([0],1,1))
  return candidates

# TODO: preprocess all candidates (e.g. pruning rules)
def preprocess(candidates):

  # PRUNING RULE 1: check if every word of candidate's text start with capital letter or not
  # for example: 'Elon Musk' is a valid name but 'Musk has' is an obvious negative
  # since 'has' starts with a small letter.
  prunedCandidatesStage1 = []
  for i in range(0, len(candidates)):
    words = []
    text = candidates[i].text
    words.extend(re.findall(r'\S+', text))
    flag = 0
    for idx, val in enumerate(words):
      if val[0].isalpha() == False or val[0].isupper() == False:
        flag = 1
        break
    if flag == 1:
      continue
    prunedCandidatesStage1.append(candidates[i]);

  # PRUNING RULE 2: Remove single word salutation candidates like Mr, Ms, Mrs and Dr
  salut = ["Mr", "Ms", "Mrs", "Dr"]
  prunedCandidatesStage2 = []
  for i in range(0, len(prunedCandidatesStage1)):
    flag = 0
    for j in range(0, len(salut)):
      if(prunedCandidatesStage1[i].text == salut[j]):
        flag = 1
        break
    if flag == 1:
      continue
    prunedCandidatesStage2.append(prunedCandidatesStage1[i]);

  # PRUNING RULE 3: Remove candidates that have prepositions and third person indirect references in them
  # Note : More can be discovered later, the following were occuring the most in the first 60 files
  prunedCandidatesStage3 = []
  prep = ["The", "To", "I", "In", "On", "His", "Her", "He", "She", "They", "With", "It", "But", "As", "A", "This", "We"]
  for i in range(0, len(prunedCandidatesStage2)):
    words = []
    text = prunedCandidatesStage2[i].text
    words.extend(re.findall(r'\S+', text))
    flag = 0
    for idx, val in enumerate(words):
      for j in range(0, len(prep)):
        if val == prep[j]:
          flag = 1
          break
      if flag == 1:
        break
    if flag == 1:
        continue
    prunedCandidatesStage3.append(prunedCandidatesStage2[i]);

  return prunedCandidatesStage3

# TODO: generate features for candidates left after pre-processing
def generateFeatures(candidates):
  return 0

# TODO: postprocess all candidates
def postprocess(candidates):
  return 0

# TODO: evaluates result
def evaluate(candidates):
  return 0

def main():
  # read files from I
  texts,labels,positions = readfile()
  #print(texts)
  #print(labels)
  candidates = generatecandiates(texts, labels,positions)
  f = open("candidatesGenerated.txt", "w")
  for i in range(0,len(candidates)):
    f.write('{} {} {}\n'.format(candidates[i].text, candidates[i].position, candidates[i].label))

  candidates = preprocess(candidates)
  f = open("candidatesPruned.txt", "w")
  count = 0
  for i in range(0,len(candidates)):
    f.write('{} {} {}\n'.format(candidates[i].text, candidates[i].position, candidates[i].label))
    if candidates[i].label != -1:
      count += 1
  print(count); #count of candidates that are valid names
  candidates = generateFeatures(candidates)
  candidates = ml.traindata(candidates,labels)
  candidates = postprocess(candidates)
  evaluate(candidates)


if __name__== "__main__":
  main()