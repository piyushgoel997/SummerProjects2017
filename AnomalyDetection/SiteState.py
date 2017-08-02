import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import random
from AnomalyDetection import *
from Preprocessing import *

# imp variables
min_occurrence = 10
max_timedelta = dt.timedelta(hours=1)
min_timedelta = dt.timedelta()
# dur = [dt.timedelta(), dt.timedelta(hours=1)]
dur = [min_timedelta, max_timedelta]
num_of_pos_examples = 1000
min_alarms = 2

# read csv
# data = pd.read_csv(r"ApolloDataPartial.csv", usecols=['SITE_ID', 'ALARM_ID', 'START_DATE', 'START_TIME'])
# # convert start and and date and times to datetime
# data['START'] = data['START_DATE'] + data['START_TIME']
# data['START'] = pd.to_datetime(data['START'], format='%d-%m-%Y%H:%M:%S')
# data = data.drop('START_DATE', axis=1)
# data = data.drop('START_TIME', axis=1)
data = pd.read_csv(r"out.csv", usecols=['SITE_ID', 'ALARM_ID', 'START'])
data['START'] = pd.to_datetime(data['START'], format='%m/%d/%Y %H:%M')
print("csv file read")

#### Make Training Dataset
all_alarms = list(set(data['ALARM_ID'].values))  # list of all possible alarm ids
X, all_alarms, listOfRemovedColumns = removeUnnecessaryColumns(
    positiveExamples(data, all_alarms, num_of_pos_examples, dur, min_alarms), all_alarms, min_occurrence)
print("dataset made")

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

m = np.shape(X)[0]  # number of examples

# taking only 50 random anomalies in the cross validation set.
random.shuffle(alarms)
Xval = makeFeatureMatrix(alarms[0:50], list(all_alarms))

# estimating the gaussian curve. mu = mean, sigma = standard deviation.
Xtrain = X[:int(0.6 * m)]
mu, sigma = estimateGaussian(Xtrain)
print("training done")

yval = np.ones((np.shape(Xval)[0], 1))
pos_ex = X[int(0.6 * m):int(0.8 * m)]
Xval = np.concatenate((Xval, pos_ex), axis=0)
yval = np.concatenate((yval, np.zeros((pos_ex.shape[0], 1))), axis=0)
print("cross validation set made")
pval = multivariateGaussian(Xval, mu, sigma)

bestEpsilon, bestF1, best, (eps, scores) = selectThreshold(pval, yval, stopAt=1 / 100, stepsize=1 / 10000)
print("training set : " + str(np.shape(Xtrain)))
print("cross validation set : " + str(np.shape(Xval)) + " (with " + str(np.size(alarms)) + " anomalies)")
print("best value of F1 score is : " + str(bestF1))
print("corresponding value of epsilon is : " + str(bestEpsilon))
print("true pos : " + str(best[0]) + "\ntrue negative : " + str(best[1]) + "\nfalse positive : " + str(
    best[2]) + "\nfalse negative : " + str(best[3]))
acc = (best[0] + best[1]) / (best[0] + best[1] + best[2] + best[3])
print("accuracy : " + str(acc))

plt.figure(figsize=(10, 10))
plt.plot(eps, scores)
plt.savefig("plot2.pdf")

#### testing

Xtest = makeFeatureMatrix(alarms[50:100], list(all_alarms))
ytest = np.ones((np.shape(Xtest)[0], 1))
pos_ex = X[int(0.8 * m):]
Xtest = np.concatenate((Xtest, pos_ex), axis=0)
ytest = np.concatenate((ytest, np.zeros((pos_ex.shape[0], 1))), axis=0)

ptest = multivariateGaussian(Xtest, mu, sigma)
f1, acc = test(ptest, ytest, bestEpsilon)
print("for testing set of size " + str(len(ytest)) + " F1 : " + str(f1) + " acc : " + str(acc))

"""
####considering site off as anomalies
also check plot2.pdf, similar situation as the previous case.####
####within 1hr####
training set : (4000, 44)
cross validation set : (1322, 44) (with 322 anomalies)
best value of F1 score is : 0.5349032800672834
corresponding value of epsilon is : 1e-08
true pos : 318          (site going off correctly detected)
true negative : 451     (correctly classified as site not going off)
false positive : 549    (falsely said the site will go off but it didn't)
false negative : 4      (unable to detect site going off)
####within 2 hrs####
training set : (4000, 47)
cross validation set : (1395, 47) (with 395 anomalies)
best value of F1 score is : 0.5540983606557376
corresponding value of epsilon is : 1e-08
true pos : 338          (site going off correctly detected)
true negative : 513     (correctly classified as site not going off)
false positive : 487    (falsely said the site will go off but it didn't)
false negative : 57     (unable to detect site going off)


training set : (16000, 56)
cross validation set : (4322, 56) (with 322 anomalies)
best value of F1 score is : 0.23584504044274154
corresponding value of epsilon is : 1e-12
true pos : 277
true negative : 2250
false positive : 1750
false negative : 45

#### for 2-3 hrs
training set : (8000, 48)
cross validation set : (2084, 48) (with 84 anomalies)
best value of F1 score is : 0.11703056768558953
corresponding value of epsilon is : 0.001
true pos : 67
true negative : 1006
false positive : 994
false negative : 17

#### changed code
#### 0-1 hrs
training set : (4000, 36)
cross validation set : (1147, 36) (with 147 anomalies)
best value of F1 score is : 0.3321799307958478
corresponding value of epsilon is : 0.001
true pos : 144
true negative : 424
false positive : 576
false negative : 3
accuracy : 0.4952048823016565

#### 1 day
training set : (800, 52)
cross validation set : (466, 52) (with 266 anomalies)
best value of F1 score is : 0.7968253968253968
corresponding value of epsilon is : 0.001
true pos : 251
true negative : 87
false positive : 113
false negative : 15
accuracy : 0.7253218884120172

#### 12 hrs
training set : (800, 48)
cross validation set : (453, 48) (with 253 anomalies)
best value of F1 score is : 0.811783960720131
corresponding value of epsilon is : 0.001
true pos : 248
true negative : 90
false positive : 110
false negative : 5
accuracy : 0.7461368653421634

training set : (1600, 57)
cross validation set : (653, 57) (with 253 anomalies)
best value of F1 score is : 0.7098591549295774
corresponding value of epsilon is : 0.001
true pos : 252
true negative : 195
false positive : 205
false negative : 1
accuracy : 0.6845329249617151

training set : (4000, 69)
cross validation set : (1253, 69) (with 253 anomalies)
best value of F1 score is : 0.4860710854947166
corresponding value of epsilon is : 0.0001
true pos : 253
true negative : 465
false positive : 535
false negative : 0
accuracy : 0.573024740622506


#### 6 hrs
training set : (800, 45)
cross validation set : (434, 45) (with 234 anomalies)
best value of F1 score is : 0.7627118644067796
corresponding value of epsilon is : 0.006
true pos : 225
true negative : 69
false positive : 131
false negative : 9
accuracy : 0.6774193548387096



12hrs
training set : (1200, 60)
cross validation set : (450, 60) (with 50 anomalies)
best value of F1 score is : 0.3125
corresponding value of epsilon is : 0.0001
true pos : 50
true negative : 180
false positive : 220
false negative : 0
accuracy : 0.5111111111111111
for testing set of size 450 F1 : 0.3194888178913738 acc : 0.5266666666666666

training set : (600, 48)
cross validation set : (250, 48) (with 253 anomalies)
best value of F1 score is : 0.47058823529411764
corresponding value of epsilon is : 0.0001
true pos : 48
true negative : 94
false positive : 106
false negative : 2
accuracy : 0.568
for testing set of size 250 F1 : 0.4694835680751174 acc : 0.548

6hrs
training set : (600, 47)
cross validation set : (250, 47) (with 234 anomalies)
best value of F1 score is : 0.42105263157894735
corresponding value of epsilon is : 0.0001
true pos : 48
true negative : 70
false positive : 130
false negative : 2
accuracy : 0.472
for testing set of size 250 F1 : 0.4343891402714932 acc : 0.5

1hr
training set : (3000, 66)
cross validation set : (1050, 66) (with 50 anomalies)
best value of F1 score is : 0.16333333333333333
corresponding value of epsilon is : 0.0001
true pos : 49
true negative : 499
false positive : 501
false negative : 1
accuracy : 0.5219047619047619
for testing set of size 1050 F1 : 0.1592356687898089 acc : 0.49714285714285716

training set : (600, 41)
cross validation set : (250, 41) (with 147 anomalies)
best value of F1 score is : 0.42608695652173906
corresponding value of epsilon is : 0.0001
true pos : 49
true negative : 69
false positive : 131
false negative : 1
accuracy : 0.472
for testing set of size 250 F1 : 0.44019138755980863 acc : 0.532

"""
