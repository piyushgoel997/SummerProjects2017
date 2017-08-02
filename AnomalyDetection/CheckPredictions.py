
def accuracy(clf, X_test, y_test):
    y_predicted = clf.predict(X_test)
    count = 0.0
    for i in range(y_test.shape[0]):
        if y_test[i] == y_predicted[i]:
            count += 1
    return (100*count)/len(y_test)


def F1_Score(clf, X_test, y_test):
    y_predicted = clf.predict(X_test)
    tp = 0.0
    tn = 0.0
    fp = 0.0
    fn = 0.0

    for i in range(y_test.shape[0]):
        if y_test[i] == y_predicted[i]:
            if y_test[i] == 1:
                tp += 1
            else:
                tn += 1
        elif y_test[i] == 1:
            fn += 1
        else:
            fp += 1

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    num = 2 * precision * recall
    den = precision + recall
    return num / den
