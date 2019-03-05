from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression

# cross validation classifer. Five classifers in total:
# 0 : decision tree
# 1 : random forest
# 2 : from sklearn import svm
# 3 : linear regression
# 4 : logistic regression
def traindata(candidates,startfile,endfile,endtestfile):
    # divide candidates into averagely five sets for developing, and last set for testing
    Xm, Xs, Ys = dividecandidates(candidates,startfile,endfile,endtestfile)

    # five classifers
    clf = []
    clf.append(tree.DecisionTreeClassifier())
    clf.append(RandomForestClassifier(n_estimators=100, max_depth=2,random_state=0))
    clf.append(svm.SVC(gamma='scale'))
    clf.append(linear_model.LinearRegression())
    clf.append(LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial', max_iter=500))

    # performance = recall + precision
    performance = []
    for i in range(5):
        performance.append(0)

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
             precision, recall = evaluate(Ytest, Yresult)
             if precision > 0.9:
                 precision = 0.9
             if recall > 0.6:
                 recall = 0.6
             performance[k] = performance[k] + precision + recall

    # find the best performance
    best = max(performance)
    bestindex = [i for i,k in enumerate(performance) if k == best]
    print("best classifer: ",bestindex[0])

    # final test
    for j in range(5):
            Xtran.extend(Xs[j])
            Ytran.extend(Ys[j])
    Xtest = Xs[5]
    Ytest = Ys[5]
    cclf = clf[0].fit(Xtran, Ytran)
    Yresult = cclf.predict(Xtest)
    postprocess(Yresult)
    precision, recall = evaluate(Ytest, Yresult)
    print("precision: ", precision)
    print("recall: ", recall)

# postprocess
# Nothing
def postprocess(Yresult):
    return

# dive files into 5 sets for cross validation
# for example, if startfile = 1, endfile = 6
# sets = [[1], [2], [3], [4], [5]]
def dividecandidates(candidates,startfile,endfile,endtestfile):
    n = int((endfile - startfile)/5)
    sets = []
    for i in range(4):
        sets.append(list(range(startfile + i * n, startfile + (i + 1) * n)))
    sets.append(list(range(startfile + 4 * n, endfile)))
    sets.append(list(range(endfile, endtestfile)))
    # Xs is inputs, Ys is outputs, Xm is for debug
    Xm = []
    for i in range(6):
        Xm.append([])
    Xs = []
    for i in range(6):
        Xs.append([])
    Ys = []
    for i in range(6):
        Ys.append([])

    # divide candidates into Xs and Ys
    for candidate in candidates:
        for i in range(6):
            if(candidate.position[0] in sets[i]):
                Xm[i].append([candidate.text, candidate.position[0],candidate.position[1]])
                Xs[i].append([candidate.position[2], candidate.length, candidate.disTosalution, candidate.disTospeak, candidate.punctuation, candidate.disTitle, candidate.disJob, candidate.nameScore])
                Ys[i].append(candidate.label)
                break
    return Xm,Xs, Ys

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
    # print(precision)
    # print(recall)
    return precision, recall
