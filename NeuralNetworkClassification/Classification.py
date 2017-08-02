import numpy as np
import pandas as pd
from sklearn.svm import SVC
import CheckPredictions
import time

print("loading data")
size = 10
path = r"smallerData.txt"


def read_data():
    # # file = open(path, 'r')
    # data = np.zeros()
    # i = 0
    # for line in file.read().split():
    #     data[i] = int(line)
    #     i += 1
    # return data

    temp = pd.read_csv(path)
    return temp.ALARM_ID


data = np.array(read_data())


def replace_with():
    for i in range(len(data)):
        if data[i] == 441 or data[i] == 442:
            data[i] = site_off


site_off = -2
replace_with()
print(data[71])

X = np.zeros((len(data), size))
y = np.zeros((len(data)))


def load_features():
    X = np.zeros((len(data), size))
    y = np.zeros((len(data)))
    for i in range(len(data) - (size + 5)):
        if site_off in data[i:i + size]:
            i += 1
            continue
        X[i] = data[i:i + size]
        if site_off in data[i + size:i + size + 3]:
            y[i] = 1
        else:
            y[i] = 0
        i += 1
    return X, y


X, y = load_features()


# saving the features to a text file - features.txt
# to avoid doing the same work again and again for testing
# file features.txt shape(no_of_samples, 1 + no_of_features)
i = 0
file = open("features.txt", 'w')
for row in X:
    if 0 in row:
        i += 1
        continue
    file.write(str(y[i]) + " ")
    i += 1
    for num in row:
        file.write(str(num) + " ")
    file.write("\n")
print("file written")


# reading features from file into the feature vector.
print("reading features")
file = open("features.txt", 'r')
file = file.read()
i = 0
for line in file.split("\n"):
    # print(len(line))
    j = 0
    flag = True
    for word in line.split(" "):
        if flag and len(word) > 0:
            y[i] = float(word)
            flag = False
        elif len(word) > 0:
            X[i, j] = float(word)
            j += 1
    i += 1
print("features read")


training_set_size = int(0.8 * len(X))

X_train = X[0:training_set_size]
y_train = y[0:training_set_size]

X_test = X[training_set_size:]
y_test = y[training_set_size:]

clf = SVC(kernel='linear', class_weight='balanced')

t = time.clock()
print(t/1000.0)
clf.fit(X_train, y_train)
t = t - time.clock()

print("classifier trained")
print(t + "," + t/1000.0)


t = time.clock()
print(CheckPredictions.accuracy(clf, X_test, y_test))
print(CheckPredictions.F1_Score(clf, X_test, y_test))
t = t - time.clock()
print(t + "," + t/1000.0)
