from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression

# cross validation classifer. Five classifers in total:
# 1 : decision tree
# 2 : random forest
# 3 : from sklearn import svm
# 4 : linear regression
# 5 : logistic regression
def traindata(candidates,startfile,endfile):
    # divide candidates into five sets
    Xs, Ys = dividecandidates(candidates,startfile,endfile)

    clf = []
    clf.append(tree.DecisionTreeClassifier())
    clf.append(RandomForestClassifier())
    clf.append(svm.SVC())
    clf.append(linear_model.LinearRegression())
    clf.append(LogisticRegression())
    # cross validation
    for k in range(len(clf)):
        for i in range(5):
             Xtran = []
             Ytran = []
             for j in range(5):
                 if j != i:
                     Xtran.extend(Xs[j])
                     Ytran.extend(Ys[j])
             Xtest = Xs[i]
             Ytest = Ys[i]
             cclf = clf[k].fit(Xtran, Ytran)
             Yresult = cclf.predict(Xtest)
             evaluate(Ytest, Yresult)

    # classifer = crossvalidation(candidates,labels,startfile,endfile)
    return 0
    # return clf

# dive files into 5 sets for cross validation
# for example, if startfile = 1, endfile = 6
# sets = [[1], [2], [3], [4], [5]]
def dividecandidates(candidates,startfile,endfile):
    n = int((endfile - startfile)/5)
    sets = []
    for i in range(4):
        sets.append(list(range(startfile + i * n, startfile + (i + 1) * n)))
    sets.append(list(range(startfile + 4 * n, endfile)))

    # Xs is inputs, Ys is outputs
    Xs = []
    for i in range(5):
        Xs.append([])
    Ys = []
    for i in range(5):
        Ys.append([])

    # divide candidates into Xs and Ys
    for candidate in candidates:
        for i in range(5):
            if(candidate.position[0] in sets[i]):
                Xs[i].append([candidate.position[2], candidate.length, candidate.disTosalution, candidate.disTospeak, candidate.punctuation, candidate.disTitle, candidate.disJob])
                Ys[i].append(candidate.label)
                break
    return Xs, Ys

def evaluate(Ytest, Yresult):
    if(len(Ytest)!= len(Yresult)):
        print("different length error!")
    truepositive = 0
    falsepositive = 0
    falsenegative = 0
    for i in range(len(Ytest)):
        if Yresult[i] == 1 and Ytest[i] == 1:
            truepositive = truepositive + 1
        elif Yresult[i] == 1 and Ytest[i] == -1:
            falsepositive = falsepositive + 1
        elif Yresult[i] == -1 and Ytest[i] == 1:
            falsenegative = falsenegative + 1

    if truepositive + falsepositive == 0:
        precision = 0
    else:
        precision = truepositive/(truepositive + falsepositive)

    if truepositive + falsenegative == 0:
        recall = 0
    else:
        recall = truepositive/(truepositive + falsenegative)

    # print(truepositive)
    # print(falsepositive)
    # print(falsenegative)
    # print()
    print(precision)
    print(recall)
    print()
