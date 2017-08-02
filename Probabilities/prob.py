import numpy as np
import operator

file = open(r"C:\Users\Piyush.CPU223\Desktop\New folder\alarms.txt")
size = 0
for line in file.read().split("\n"):
    if len(line) != 0:
        size += 1;

alarms = np.zeros(size)
i = 0
file = open(r"C:\Users\Piyush.CPU223\Desktop\New folder\alarms.txt")
for line in file.read().split("\n"):
    if len(line) != 0:
        alarms[i] = line
        i += 1

count = {}
lcount = {}
prev = -1
l = -1
for i in alarms:
    if i not in count:
        count[i] = (i, 0, 0, 0)
        lcount[i] = (i, 0, 0, 0)
    (b, x, y, z) = count[i]
    count[i] = (b, x + 1, y, z)
    (b, x, y, z) = lcount[i]
    lcount[i] = (b, x + 1, y, z)
    if i == 441:
        (b, x, y, z) = count[prev]
        count[prev] = (b, x, y + 1, z)
        (b, x, y, z) = lcount[l]
        lcount[l] = (b, x, y + 1, z)
    if i == 442:
        (b, x, y, z) = count[prev]
        count[prev] = (b, x, y, z + 1)
        (b, x, y, z) = lcount[l]
        lcount[l] = (b, x, y, z + 1)
    l = prev
    prev = i

prob = {}  #
ct = 0  #
prob2 = {}
lprob = {}
lprob2 = {}
for i in count.keys():
    (b, x, y, z) = count[i]
    # count[i] = (b, x, y/649, z/293)
    prob[ct] = (b, (y + z) / 1000)  #
    prob2[ct] = (b, (y + z) / x)
    (b, x, y, z) = lcount[i]
    lprob[ct] = (b, (y + z) / 1000)
    lprob2[ct] = (b, (y + z) / x)
    ct += 1
    # count[i] = (b, x, (y * 10000) / (649 * x), (z * 10000) / (293 * x))

# probabilityMat = list(count.values())
#
# probabilityMat = sorted(probabilityMat, key=operator.itemgetter(3))

P = {}
Q = {}
for i in range(ct):
    (b, val) = prob[i]
    (b, lval) = lprob[i]
    P[i] = (b, (val + lval))

    (b, val) = prob2[i]
    (b, lval) = lprob2[i]
    Q[i] = (b, (val + lval))

# prob = sorted(prob.values(), key=operator.itemgetter(1))
# prob2 = sorted(prob2.values(), key=operator.itemgetter(1))
# lprob = sorted(lprob.values(), key=operator.itemgetter(1))
# P = sorted(P.values(), key=operator.itemgetter(1))
# Q = sorted(Q.values(), key=operator.itemgetter(1))


# for (x, y) in prob:
#     if y == 0:
#         print(str(x))

# print(prob[-10:])
# print(lprob[-10:])
# print(P[-10:])
# print(Q[-10:])

probabilities = {}

for i in range(ct):
    (b, p) = P[i]
    (b, q) = Q[i]
    probabilities[i] = (b, p, q)

probabilities = list(reversed(sorted(probabilities.values(), key=operator.itemgetter(1))))
print(probabilities)

file = open("output.txt", "w")
for i in probabilities:
    file.write(str(i))
    file.write("\n")

