import pandas as pd
from difflib import SequenceMatcher

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def longest_common_substring(s1, word):
    # Initially we can go as far to the left as we want
    left_most_valid = 0
    longest = 0
    last_seen = {}

    for i, letter in enumerate(word):
        if letter in last_seen:
            # left_most_valid must be greater than any position which has been seen again
            left_most_valid = max(left_most_valid, last_seen[letter] + 1)
        last_seen[letter] = i

        # Length of substring from left_most_valid to i is i - left_most_valid + 1
        longest = max(longest, i - left_most_valid + 1)

    return longest


def main():
    # A = "5 Steps to a 5: AP Computer Science a 2019"
    # B = "AP computer science A 2019"
    # match = SequenceMatcher(None, A.lower(), B.lower()).find_longest_match(0, len(A), 0, len(B))
    # print(match.size)
    dfA = pd.read_csv('tableA.xls', header=None)
    dfB = pd.read_csv('tableB.xls', header=None)
    f = open("candidateafterblock.csv", "a")
    f.write("A_id,B_id\n")


    i = 0
    for index1, row1 in dfA.iterrows():
        if i == 0:
            i += 1
            continue
        print(i)
        k = 0
        for index2, row2 in dfB.iterrows():
            if k == 0:
                k += 1
                continue
            # elif k % 100 == 0:
            #     print(k)
            if not (len(row1[2])/len(row2[2]) > 2 or len(row1[2])/len(row2[2]) < 0.5):
                match = SequenceMatcher(None, row1[2].lower(), row2[2].lower()).find_longest_match(0, len(row1[2]), 0, len(row2[2]))
                if match.size/max(len(row1[2]),len(row2[2])) > 0.5:
                    f.write(str(row1[0]) + "," + str(row2[0]) + "\n")
                    continue
            if (abs(len(row1[2])-len(row2[2])) < 5) and (levenshteinDistance(row1[2].lower(),row2[2].lower()) < 5):
                f.write(str(row1[0]) + "," + str(row2[0]) + "\n")
            k += 1
        i = i + 1
    f.close()
if __name__== "__main__":
    main()
