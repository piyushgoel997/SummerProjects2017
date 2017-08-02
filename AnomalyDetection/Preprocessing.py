import numpy as np

listOfRemovedColumns = []


def removeUnnecessaryColumns(X, all_alarms, min_occurrence):
    m, n = np.shape(X)
    Xnew = []
    for col in range(n):
        if np.sum(X[:, col]) >= min_occurrence:
            Xnew.append(X[:, col])
        else:
            listOfRemovedColumns.append(col)
    list_to_remove = []
    for i in listOfRemovedColumns:
        list_to_remove.append(all_alarms[i])
    all_alarms = np.array(list(set(all_alarms).difference(set(list_to_remove))))
    return np.transpose(Xnew), all_alarms, list_to_remove


def makeFeatureMatrix(alarms, all_alarms):
    m = len(alarms)
    n = len(all_alarms)
    X = np.zeros((m, n))
    for i in range(m):
        for a in alarms[i]:
            if a in all_alarms:
                X[i, all_alarms.index(a)] = 1
    return X


def positiveExamples(data, all_alarms, m, dur, min_alarms):
    """
    :param data: pandas DataFrame containing all of the data.
    :param all_alarms: list of included alarms.
    :param m: number of positive examples required.
    :param dur: a tuple of size 2 of the min and max duration for the alarms to be checked in.
    :param min_alarms: min number of alarms that should have occurred in the duration.
   :return: X: feature matrix of positive examples.
    """
    alarms = []
    # Just just get the lists of alarms for m examples and feed it to makeFeatureMatrix function.
    import random
    i = 0
    while i < m:
        idx = random.randrange(data.shape[0])
        curr = list(set(data[
                            (data.loc[idx]["SITE_ID"] == data["SITE_ID"]) & (
                                ((data.loc[idx]['START'] - data['START'] < dur[1]) & (
                                    data.loc[idx]['START'] - data['START'] > dur[0])))]["ALARM_ID"].values))
        for a in curr:
            if a not in all_alarms:
                curr.remove(a)
        next_alarms = list(set(data[(data.loc[idx]["SITE_ID"] == data["SITE_ID"]) & (
                data["START"] - data.loc[idx]["START"] < dur[1]) & (
                    data["START"] - data.loc[idx]["START"] > dur[0])]["ALARM_ID"].values))
        if (len(curr) >= min_alarms) and (441 not in next_alarms):
            alarms.append(curr)
            i += 1
            print(i)
    return makeFeatureMatrix(alarms, list(all_alarms))
