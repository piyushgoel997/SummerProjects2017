import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from AnomalyDetection import estimateGaussian
from AnomalyDetection import multivariateGaussian
from AnomalyDetection import selectThreshold
from Preprocessing import makeFeatureMatrix
from Preprocessing import removeUnnecessaryColumns
from Preprocessing import positiveExamples

# imp variables

min_occurrence = 10
n_pos = 50  # number of positive examples for cross validation set.
max_timedelta = dt.timedelta(hours=2)
min_timedelta = dt.timedelta()
dur = [min_timedelta, max_timedelta]
min_alarms = 2

# read csv
data = pd.read_csv(r"ApolloDataPartial.csv", usecols=['SITE_ID', 'ALARM_ID', 'START_DATE', 'START_TIME'])
# convert start and and date and times to pd datetime
data['START'] = data['START_DATE'] + data['START_TIME']
data['START'] = pd.to_datetime(data['START'], format='%d-%m-%Y%H:%M:%S')
data = data.drop('START_DATE', axis=1)
data = data.drop('START_TIME', axis=1)
print("csv file read")

# indices of all rows containing 441
indices = data[data['ALARM_ID'] == 441].index

# list of lists of alarms occurring one hr before 441
alarms = []
for i in indices:
    ai = (list(set(data[
                       (data['SITE_ID'] == data.loc[i].SITE_ID) & (
                           data.loc[i].START - data['START'] < max_timedelta) & (
                           data.loc[i].START - data['START'] > min_timedelta)]['ALARM_ID'].values)))
    if len(ai) >= min_alarms:
        alarms.append(ai)

all_alarms = list(set(data['ALARM_ID'].values))  # list of all possible alarm ids

m = len(alarms)  # number of examples

X, all_alarms, listOfRemovedColumns = removeUnnecessaryColumns(makeFeatureMatrix(alarms, all_alarms), all_alarms,
                                                               min_occurrence)
print("pre processing done")

# X = np.zeros((m, n))
# for i in range(m):
#     for a in alarms[i]:
#         X[i, all_alarms.index(a)] = 1


# # remove this part. Later.
# file = open('list.txt', 'w')
# for item in X:
#     file.write("%s\n" % item)

# estimating the gaussian curve. mu = mean, sigma = standard deviation.
fullX = X
X = X[:int(0.7 * m)]
mu, sigma = estimateGaussian(X)
p = multivariateGaussian(X, mu, sigma)
print("training done")

Xval = fullX[0.7 * m:]
yval = np.zeros((np.shape(Xval)[0], 1))
pos_ex = positiveExamples(data, all_alarms, n_pos, dur, min_alarms)
Xval = np.concatenate((Xval, pos_ex), axis=0)
yval = np.concatenate((yval, np.ones((pos_ex.shape[0], 1))), axis=0)
print("cross validation set made")
mu_val, sigma_val = estimateGaussian(Xval)
pval = multivariateGaussian(Xval, mu_val, sigma_val)

bestEpsilon, bestF1, best, (eps, scores) = selectThreshold(pval, yval, stopAt=1/1000, stepsize=1/10000000)
print("training set : " + str(np.shape(X)))
print("cross validation set : " + str(np.shape(Xval)) + " (with " + str(n_pos) + " anomalies)")
print("best value of F1 score is : " + str(bestF1))
print("corresponding value of epsilon is : " + str(bestEpsilon))
print("true pos : " + str(best[0]) + "\ntrue negative : " + str(best[1]) + "\nfalse positive : " + str(
    best[2]) + "\nfalse negative : " + str(best[3]))


plt.figure(figsize=(10, 10))
plt.plot(eps, scores, "b-")
plt.savefig("plot1.pdf")
"""
####considering site not off as anomalies
also check plot1.pdf, which shows that changing epsilon will have no effect on the F1 score after a certain limit(verified manually also).
i.e. there are some cases which will always be wrongly classified.
So, some particular faulty cases need to be removed from the training data, which is a quite difficult task.
And only the changes in the input data will affect the resulting score.####
####within 1hr####
training set : (225, 14)
cross validation set : (147, 14) (with 50 anomalies)
best value of F1 score is : 0.6229508196721312
corresponding value of epsilon is : 0.0002781
true pos : 38        (correctly classified as site not going off)
true negative : 63   (site going off correctly detected)
false positive : 34  (unable to detect site going off)
false negative : 12  (falsely said the site will go off but it didn't)
####within 2 hrs####
training set : (276, 22)
cross validation set : (169, 22) (with 50 anomalies)
best value of F1 score is : 0.6068965517241379
corresponding value of epsilon is : 0.0006133
true pos : 44        (correctly classified as site not going off)
true negative : 68   (site going off correctly detected)
false positive : 51  (unable to detect site going off)
false negative : 6   (falsely said the site will go off but it didn't)
"""