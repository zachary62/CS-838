import re
import ml

# startfile  =  2
# endfile = 3
startfile  =  1
endfile = 201
endtestfile = 301
common_names = []

# candidate of all sub strings
class candidate:
    def __init__(self, text, position, label, length, disTosalution, disTospeak, punctuation, disTitle, disJob, nameScore):
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
        # The first feature is the total length of string
        # for example "Mr Elon Musk has Three Wives"
        # "Mr" : 2
        # "Mr Elon" : 7
        self.length = length
        # The distance to salutions including ["Mr", "Ms", "Mrs", "Dr", "Miss", "Mx", "Sir"]
        # distance is at most 5. Otherwise, distance is 999
        # if the candidate text contain one of these titles, distance is zero
        # for example "Mr Elon Musk has Three Wives, bla bla bla bla bla Time"
        # "Mr Elon Musk" : 0
        # "Elon Musk" : 1
        # "Three" : 4
        # "Time" : 999
        self.disTosalution = disTosalution
        # The distance to speak actions including ["say","says","said","tell","tells","told","asks","asked","speak","speaks","spoken"]
        # distance is at most 5. Otherwise, distance is 999
        # if the candidate text contain one of these titles, distance is zero
        # for example "Mr Elon Musk speaks to his Three Wives, bla bla bla bla bla Time"
        # "Mr Elon Musk" : 1
        # "Elon Musk" : 1
        # "Three" : 3
        # "Time" : 999
        self.disTospeak = disTospeak
        # Whether there is a punctuation in the middle and at the end of substring
        # true = 1 and false = -1
        # for example "Elon Musk, Alex Fust speak to their wives"
        # "Elon Musk," : -1
        # "Musk, Alex" : 1
        # "Musk, Alex Fust" : 1
        self.punctuation = punctuation
        # The distance to titles = ["Chairman", "Executive", "President", "Minister"]
        # distance is at most 5. Otherwise, distance is 999
        # for example "Chairman Mr Elon Musk speaks to his Three Wives"
        # "Mr Elon Musk" : 1
        # "Elon Musk" : 2
        self.disTitle = disTitle
        # The distance to jobs
        # jobs are string ended with ["er","or","st"]
        # for example, cooker, director, analyst
        # for example "Cooker Mr Elon Musk speaks to his Three Wive"
        # "Mr Elon Musk" : 1
        # "Elon Musk" : 2
        self.disJob = disJob
        # Scoring function for checking how many words belong to common names / length of candidate
        # +1 for every word that is in dictionary, 0 for every word not in dictionary
        # 'Elon Musk': 2/2
        # 'Elon says': 1/2
        self.nameScore = nameScore

# read files from I
# return text and labeled entity position
def readfile():
  # texts of all files
  texts = []
  labels = []
  positions = []
  # read files from I
  for i in range(startfile,endtestfile):
    file = str(i).zfill(3)
    f = open("../documents/" + file + "l.txt", "r", encoding='utf-8-sig')

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


def load_common_names():
  global common_names
  names_txt = open("names.txt", 'r')
  for name in names_txt:
    common_names.append(name[:-1])


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
      candidates.append(candidate(text, pos, labels[k][i], 1, 1, 1, 1, 1, 1, 0.0))

  # #generate candidates of length 2
  # for k in range(0,len(texts)):
  #   for i in range(0,len(texts[k]) - 1):
  #     text = texts[k][i] + " " + texts[k][i+1]
  #     pos = []
  #     pos.append(k+1)
  #     pos.append(positions[k][i])
  #     pos.append(2)
  #
  #     punctuation = [',','.','?','!',':','\'','\"','(',')',';']
  #     if labels[k][i] != -1 and labels[k][i+1] != -1:
  #       #this is a probable candidate name of length 2 words
  #       if texts[k][i][-1:] in punctuation :
  #         # for strings like "Elon Musk, Mark Manson and Tom Sawyer are good friends.", candidates are generated as
  #         # Elon Musk, ; Musk, Mark and so on; so we need to avoid combining two names together like in Musk, Mark;
  #         # if a comma is encountered in probable candidate generation that indicates one name ended and another name started, then that
  #         # is marked as not a name
  #         label = -1
  #       else:
  #         label = labels[k][i]
  #     else:
  #       label = -1 #includes cases like "Musk has" or "said Elon" where one of the word is not a name and cases like "has three" where none of the word is a name
  #
  #     candidates.append(candidate(text, pos, label, 1, 1, 1, 1, 1, 1))
  #
  # #generate candidates of length 3
  # for k in range(0,len(texts)):
  #   for i in range(0,len(texts[k]) - 2):
  #     text = texts[k][i] + " " + texts[k][i+1] + " " + texts[k][i+2]
  #     pos = []
  #     pos.append(k+1)
  #     pos.append(positions[k][i])
  #     pos.append(3)
  #
  #     if labels[k][i] != -1 and labels[k][i+1] != -1 and labels[k][i+2] != -1:
  #       #this is a probable candidate name of length 3 words
  #       if texts[k][i][-1:] in punctuation or texts[k][i+1][-1:] in punctuation:
  #         # for strings like "Elon Musk, Mark Manson and Tom Sawyer are good friends.", candidates are generated as
  #         # Elon Musk, Mark ; Musk, Mark Manson and so on; so we need to avoid combining two names together
  #         # if a comma is encountered in probable candidate generation that indicates one name ended and another name started, then that
  #         # is marked as not a name
  #         label = -1
  #       else:
  #         label = labels[k][i]
  #     else:
  #       # includes cases like 'Musk has three' or 'said Elon Musk' where one of the word is not a name
  #       # and cases like 'has three wives' where none of the word is a name
  #       label = -1
  #
  #     candidates.append(candidate(text, pos, label, 1, 1, 1, 1, 1, 1))

  #candidates.append(candidate([0],1,1))
  #candidates.append(candidate([0],1,1))
  return candidates

# preprocess all candidates (e.g. pruning rules)
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

  # PRUNING RULE 2: Remove titles like Chairman, Executive, President, Minister
  titles = ["Chairman", "Executive", "President", "Minister","Chief","Boss","Spokesman","Secretary","General","Judge"]
  prunedCandidatesStage2 = []
  for i in range(0, len(prunedCandidatesStage1)):
    flag = 0
    for j in range(0, len(titles)):
      if(prunedCandidatesStage1[i].text == titles[j]):
        flag = 1
        break
    if flag == 1:
      continue
    prunedCandidatesStage2.append(prunedCandidatesStage1[i]);

  # PRUNING RULE 3: Remove candidates that have prepositions and third person indirect references in them
  # Note : More can be discovered later, the following were occuring the most in the first 60 files
  prunedCandidatesStage3 = []
  prep = ["The","To","I","In","On","His","Her","He","She","They","With","It","But","As","A","This","We","However","For","Before","After","Although","Vice","Former","Prime","Treasury","Under"]
  country = ["America", "American", "Africa","African","United States", "German","Germany","India","Indian","Britain","British","China","Chinese","Korean", "Japan", "Japanese", "Russia","Russian","Swiss"]
  for i in range(0, len(prunedCandidatesStage2)):
    words = []
    text = prunedCandidatesStage2[i].text
    words.extend(re.findall(r'\S+', text))
    flag = 0
    for idx, val in enumerate(words):
      if val in prep or val in country:
          flag = 1
          break
    if flag == 1:
        continue
    prunedCandidatesStage3.append(prunedCandidatesStage2[i]);

  return prunedCandidatesStage3

# generate features for candidates left after pre-processing
def generateFeatures(candidates, texts):
  for candidate in candidates:
    # first feature: length of candidate text
    candidate.length = len(candidate.text)

    # second feature: disTosalution
    # The distance to previous salutions including ["Mr", "Ms", "Mrs", "Dr", "Miss", "Mx", "Sir"]
    # distance is at most 5. Otherwise, distance is 999
    # if the candidate text contain one of these titles, distance is zero
    # for example "Mr Elon Musk has Three Wives, bla bla bla bla bla Time"
    # "Mr Elon Musk" : 0
    # "Elon Musk" : 1
    # "Three" : 4
    # "Time" : 999
    words = []
    sals = ["Mr", "Ms", "Mrs", "Dr", "Miss", "Mx", "Sir"]
    text = candidate.text
    words.extend(re.findall(r'\S+', text))
    for word in words:
        if word in sals:
          candidate.disTosalution = 0
    # if not included, check distance
    if candidate.disTosalution != 0:
      if (candidate.position[1] >= 1 and texts[candidate.position[0] - 1][candidate.position[1] - 1] in sals):
        candidate.disTosalution = 1
      elif (candidate.position[1] >= 2 and texts[candidate.position[0] - 1][candidate.position[1] - 2] in sals):
        candidate.disTosalution = 2
      # elif (candidate.position[1] >= 3 and texts[candidate.position[0] - 1][candidate.position[1] - 3] in sals):
      #   candidate.disTosalution = 3
      # elif (candidate.position[1] >= 4 and texts[candidate.position[0] - 1][candidate.position[1] - 4] in sals):
      #   candidate.disTosalution = 4
      # elif (candidate.position[1] >= 5 and texts[candidate.position[0] - 1][candidate.position[1] - 5] in sals):
      #   candidate.disTosalution = 5
      else:
        candidate.disTosalution = 999

    # second feature: disTospeak
    # The distance to speak actions including ["say","says","said","tell","tells","told","asks","asked","speak","speaks","spoken"]
    # distance is at most 5. Otherwise, distance is 999
    # if the candidate text contain one of these titles, distance is zero
    # for example "Mr Elon Musk speaks to his Three Wives, bla bla bla bla bla Time"
    # "Mr Elon Musk" : 1
    # "Elon Musk" : 1
    # "Three" : 3
    # "Time" : 999
    speaks = ["say","says","said","tell","tells","told","asks","asked","speak","speaks","spoken","explain","explains","explained","Say","Says","Said","Tell","Tells","Told","Asks","Asked","Speak","Speaks","Spoken","Explain","Explains","Explained"]
    for word in words:
        if word in speaks:
          candidate.disTospeak = 0
    if candidate.disTospeak != 0:
      if (candidate.position[1] >= 1 and texts[candidate.position[0] - 1][candidate.position[1] - 1] in speaks) or (candidate.position[1] + candidate.position[2] <= len(texts[candidate.position[0] - 1]) - 1 and texts[candidate.position[0] - 1][candidate.position[1] + candidate.position[2]] in speaks):
        candidate.disTospeak = 1
      elif (candidate.position[1] >= 2 and texts[candidate.position[0] - 1][candidate.position[1] - 2] in speaks) or (candidate.position[1] + candidate.position[2] <= len(texts[candidate.position[0] - 1]) - 2 and texts[candidate.position[0] - 1][candidate.position[1] + candidate.position[2] + 1] in speaks):
        candidate.disTospeak = 2
      # elif (candidate.position[1] >= 3 and texts[candidate.position[0] - 1][candidate.position[1] - 3] in speaks) or (candidate.position[1] + candidate.position[2] <= len(texts[candidate.position[0] - 1]) - 3 and texts[candidate.position[0] - 1][candidate.position[1] + candidate.position[2] + 2] in speaks):
      #   candidate.disTospeak = 3
      # elif (candidate.position[1] >= 4 and texts[candidate.position[0] - 1][candidate.position[1] - 4] in speaks) or (candidate.position[1] + candidate.position[2] <= len(texts[candidate.position[0] - 1]) - 4 and texts[candidate.position[0] - 1][candidate.position[1] + candidate.position[2] + 3] in speaks):
      #   candidate.disTospeak = 4
      # elif (candidate.position[1] >= 5 and texts[candidate.position[0] - 1][candidate.position[1] - 5] in speaks) or (candidate.position[1] + candidate.position[2] <= len(texts[candidate.position[0] - 1]) - 5 and texts[candidate.position[0] - 1][candidate.position[1] + candidate.position[2] + 4] in speaks):
      #   candidate.disTospeak = 5
      else:
        candidate.disTospeak = 999

    # Third feature: punctuation
    # Whether there is a punctuation in the middle and at the end of substring
    # true = 1 and false = -1
    # for example "Elon Musk, Alex Fust speak to their wives"
    # "Elon Musk," : -1
    # "Musk, Alex" : 1
    # "Musk, Alex Fust" : 1
    punctuation = [',','.','?','!',':','\'','\"','(',')',';']
    if(candidate.position[2] == 2 and words[0][-1:] in punctuation):
      candidate.punctuation = 1
    elif(candidate.position[2] == 3 and (words[0][-1:] in punctuation or words[1][-1:] in punctuation)):
      candidate.punctuation = 1
    else:
      candidate.punctuation = -1

    # forth feature: disTitle
    # The distance to titles = ["Chairman", "Executive", "President", "Minister"]
    # distance is at most 5. Otherwise, distance is 999
    # for example "Chairman Mr Elon Musk speaks to his Three Wives"
    # "Mr Elon Musk" : 1
    # "Elon Musk" : 2
    titles = ["Chairman", "Executive", "President", "Minister","Chief","Boss","Spokesman","Secretary","General","Judge","chairman", "executive", "president", "minister","chief","boss","spokesman","secretary","general","judge"]
    for word in words:
        if word in titles:
          candidate.disTitle = -1
    if candidate.disTitle != 0:
      if (candidate.position[1] >= 1 and texts[candidate.position[0] - 1][candidate.position[1] - 1] in titles) or (candidate.position[1] + candidate.position[2] <= len(texts[candidate.position[0] - 1]) - 1 and texts[candidate.position[0] - 1][candidate.position[1] + candidate.position[2]] in titles):
        candidate.disTitle = 1
      elif (candidate.position[1] >= 2 and texts[candidate.position[0] - 1][candidate.position[1] - 2] in titles) or (candidate.position[1] + candidate.position[2] <= len(texts[candidate.position[0] - 1]) - 2 and texts[candidate.position[0] - 1][candidate.position[1] + candidate.position[2] + 1] in titles):
        candidate.disTitle = 2
      # elif (candidate.position[1] >= 3 and texts[candidate.position[0] - 1][candidate.position[1] - 3] in titles) or (candidate.position[1] + candidate.position[2] <= len(texts[candidate.position[0] - 1]) - 3 and texts[candidate.position[0] - 1][candidate.position[1] + candidate.position[2] + 2] in titles):
      #   candidate.disTitle = 3
      # elif (candidate.position[1] >= 4 and texts[candidate.position[0] - 1][candidate.position[1] - 4] in titles) or (candidate.position[1] + candidate.position[2] <= len(texts[candidate.position[0] - 1]) - 4 and texts[candidate.position[0] - 1][candidate.position[1] + candidate.position[2] + 3] in titles):
      #   candidate.disTitle = 4
      # elif (candidate.position[1] >= 5 and texts[candidate.position[0] - 1][candidate.position[1] - 5] in titles) or (candidate.position[1] + candidate.position[2] <= len(texts[candidate.position[0] - 1]) - 5 and texts[candidate.position[0] - 1][candidate.position[1] + candidate.position[2] + 4] in titles):
      #   candidate.disTitle = 5
      else:
        candidate.disTitle = 999

    # The distance to jobs
    # jobs are string ended with ["er","or","st"]
    # for example, cooker, director, analyst
    # for example "Cooker Mr Elon Musk speaks to his Three Wive"
    # "Mr Elon Musk" : 1
    # "Elon Musk" : 2
    jobs = ["er","or","st"]
    for word in words:
      if word[-2:] in jobs:
        candidate.disJob = -1
    if candidate.disJob != 0:
      if (candidate.position[1] >= 1 and texts[candidate.position[0] - 1][candidate.position[1] - 1][-2:] in jobs) or (candidate.position[1] + candidate.position[2] <= len(texts[candidate.position[0] - 1]) - 1 and texts[candidate.position[0] - 1][candidate.position[1] + candidate.position[2]][-2:] in jobs):
        candidate.disJob = 1
      elif (candidate.position[1] >= 2 and texts[candidate.position[0] - 1][candidate.position[1] - 2][-2:] in jobs) or (candidate.position[1] + candidate.position[2] <= len(texts[candidate.position[0] - 1]) - 2 and texts[candidate.position[0] - 1][candidate.position[1] + candidate.position[2] + 1][-2:] in jobs):
        candidate.disJob = 2
      # elif (candidate.position[1] >= 3 and texts[candidate.position[0] - 1][candidate.position[1] - 3][-2:] in jobs) or (candidate.position[1] + candidate.position[2] <= len(texts[candidate.position[0] - 1]) - 3 and texts[candidate.position[0] - 1][candidate.position[1] + candidate.position[2] + 2][-2:] in jobs):
      #   candidate.disJob = 3
      # elif (candidate.position[1] >= 4 and texts[candidate.position[0] - 1][candidate.position[1] - 4][-2:] in jobs) or (candidate.position[1] + candidate.position[2] <= len(texts[candidate.position[0] - 1]) - 4 and texts[candidate.position[0] - 1][candidate.position[1] + candidate.position[2] + 3][-2:] in jobs):
      #   candidate.disJob = 4
      # elif (candidate.position[1] >= 5 and texts[candidate.position[0] - 1][candidate.position[1] - 5][-2:] in jobs) or (candidate.position[1] + candidate.position[2] <= len(texts[candidate.position[0] - 1]) - 5 and texts[candidate.position[0] - 1][candidate.position[1] + candidate.position[2] + 4][-2:] in jobs):
      #   candidate.disJob = 5
      else:
        candidate.disJob = 999

      # Scoring of candidate based on whether it's in common name dictionary
      for word in words:
        if word in common_names:
          candidate.nameScore += 1
      candidate.nameScore = candidate.nameScore * 1.0 / len(words)

  return candidates

# TODO: postprocess all candidates
def postprocess(candidates):
  return 0

# TODO: evaluates result
def evaluate(candidates):
  return 0

def main():
  # read files from I
  texts,labels,positions = readfile()
  load_common_names()
  # print(texts)
  # print(positions)
  candidates = generatecandiates(texts, labels, positions)
  f = open("candidatesGenerated.txt", "w", encoding='utf-8-sig')
  for i in range(0,len(candidates)):
    f.write('{} {} {}\n'.format(candidates[i].text, candidates[i].position, candidates[i].label))

  candidates = preprocess(candidates)
  candidates = generateFeatures(candidates, texts)
  f = open("candidatesPruned.txt", "w", encoding='utf-8-sig')
  count = 0
  Icount = 0
  Jcount = 0
  for i in range(0,len(candidates)):
    f.write('{} {} {} {} {} {} {} {} {}\n'.format(candidates[i].text, candidates[i].position, candidates[i].label, candidates[i].length, candidates[i].disTosalution, candidates[i].disTospeak, candidates[i].punctuation, candidates[i].disTitle, candidates[i].disJob))
    if candidates[i].label != -1:
      count += 1
    if candidates[i].position[0] in range(startfile,endfile) and candidates[i].label != -1:
      Icount += 1
    if candidates[i].position[0] in range(endfile,endtestfile) and candidates[i].label != -1:
      Jcount += 1

  print("total number of mentions: ", count); #count of candidates that are valid names
  print("total number of mentions in I: ", Icount);
  print("total number of mentions in J: ", Jcount); 
  ml.traindata(candidates,startfile,endfile,endtestfile)
  # print(clf.predict([[2,10,0,1]]))
  # candidates = postprocess(candidates)
  #ml.evaluate(candidates)


if __name__== "__main__":
  main()
