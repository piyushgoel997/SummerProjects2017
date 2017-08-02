import numpy as np
import math


def estimateGaussian(X):
    m, n = np.shape(X)
    mu = np.transpose(np.sum(X, axis=0))
    mu /= m
    temp = np.zeros(np.shape(X))
    for i in range(np.shape(temp)[0]):
        temp[i, :] -= mu
    temp *= temp
    sigma = np.transpose(np.sum(temp, axis=0))
    sigma /= m
    return mu, sigma


def multivariateGaussian(X, mu, sigma):
    """
    :param X: feature matrix.
    :param mu: mean values of each feature stored in a vertical vector.
    :param sigma: standard deviation of each feature in a vertical vector.
    :return: probability calculated in a multivariate gaussian distribution.
    """
    m, n = np.shape(X)
    covariance_matrix = np.zeros((n, n))
    for i in range(n):
        covariance_matrix[i, i] = sigma[i]
    k = math.pow(2 * math.pi, -n / 2) * np.power(np.linalg.det(covariance_matrix), -0.5)
    mu = np.transpose(mu)
    prob = np.zeros((m, 1))
    for i in range(m):
        exp = -0.5 * ((X[i] - mu).dot(np.linalg.inv(covariance_matrix))).dot(np.transpose(X[i] - mu))
        prob[i, 0] = k * math.exp(exp)
    mu = np.transpose(mu)
    return prob


def selectThreshold(pval, yval, stopAt=1, stepsize=1 / 1000):
    """
    :param stopAt: highest value of epsilon to be considered
    :param stepsize: size of the steps to be taken while iterating epsilon
    :param pval: vertical vector containing the predicted outcomes of the cross validation set.
    :param yval: vertical vector containing the actual outcomes of the cross validation set.
    :return: that value of epsilon(threshold) for which the F1 score is maximum and the corr values of F1 score and other variables
    """
    bestEpsilon = 0
    bestF1 = 0
    bestCase = (0, 0, 0, 0)
    #####
    eps = []
    scores = []
    #####
    for epsilon in np.arange(0, stopAt, stepsize):
        predictions = np.zeros((np.shape(yval)[0], 1))
        for i in range(np.size(yval)):
            if pval[i, 0] < epsilon:
                predictions[i, 0] = 1
            else:
                predictions[i, 0] = 0

        tp = 0  # true positive
        fp = 0  # false positive
        fn = 0  # false negative
        tn = 0  # true negative

        for i in range(np.size(predictions)):
            if predictions[i, 0] == yval[i, 0]:
                if predictions[i, 0] == 1:
                    tp += 1
                else:
                    tn += 1
            else:
                if predictions[i, 0] == 1:
                    fp += 1
                else:
                    fn += 1
        if tp != 0:
            p = tp / (tp + fp)  # precision
            r = tp / (tp + fn)  # recall

            F1 = (2 * p * r) / (p + r)
        else:
            F1 = 0
        if F1 > bestF1:
            bestCase = (tp, tn, fp, fn)
            bestF1 = F1
            bestEpsilon = epsilon

        #####
        eps.append(epsilon)
        scores.append(F1)
        #####
    return bestEpsilon, bestF1, bestCase, (eps, scores)


def test(ptest, ytest, epsilon):
    tp = 0  # true positive
    fp = 0  # false positive
    fn = 0  # false negative
    tn = 0  # true negative

    for i in range(len(ptest)):
        p = ptest[i]
        y = ytest[i]
        if p < epsilon:
            if y == 1:
                tp += 1
            else:
                fp += 1
        else:
            if y == 1:
                fn += 1
            else:
                tn += 1

    p = tp / (tp + fp)
    r = tp / (tp + fn)
    F1 = (2 * p * r) / (p + r)
    acc = (tp + tn) / (tp + tn + fp + fn)
    return F1, acc
