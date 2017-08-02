import networkx as nx
from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt
import numpy as np


def best_route(sites, site_coordinates, current_loc=None, approx_sol=True):
    G = nx.Graph()
    # max() is used to convert the value of the site id to a string
    # if current_loc is str:
    #     sites.append(current_loc)
    current_loc = sites[0]
    # sites = list(set(sites))  # remove duplicates
    for i in range(len(sites)):
        # getting the co-ordinates of both sites
        # eg. - site_data.loc[site_data["S_ID"] == sites[i]] = [['ASMO_0153', 16.142670000000003, 97.72678]]
        a = site_coordinates.loc[site_coordinates["S_ID"] == sites[i]].values[0]
        for j in range(i, len(sites)):
            b = site_coordinates.loc[site_coordinates["S_ID"] == sites[j]].values[0]
            wt = geographical_distance((a[1], a[2]), (b[1], b[2]))
            G.add_edge(sites[i], sites[j], weight=wt)
    if approx_sol:
        return find_approximate_route(current_loc, G)
    return find_best_route(current_loc, G)


def geographical_distance(a, b):
    """
    :param a: tuple containing co-ordinates of the first location. ex - (16.142670000000003, 97.72678).
    :param b: tuple containing co-ordinates of the second location.
    :return: geographical_distance between the two co-ordinates.
    :see: https://stackoverflow.com/a/19412565
    """

    R = 6373.0

    lat1 = radians(a[0])
    lon1 = radians(a[1])
    lat2 = radians(b[0])
    lon2 = radians(b[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def plot_route(route, filler, site_coordinates, approx_sol=True, original_path=False):
    coordinates = np.zeros((len(route), 2))
    i = 0

    for loc in route:
        a = site_coordinates.loc[site_coordinates["S_ID"] == loc].values[0]  # see best route code for example.
        coordinates[i, 0] = a[1]
        coordinates[i, 1] = a[2]
        i += 1

    plt.figure()
    plt.xlabel("Latitude")
    plt.ylabel("Longitude")
    plt.xlim([coordinates[:, 0].min(), coordinates[:, 0].max()])
    plt.ylim([coordinates[:, 1].min(), coordinates[:, 1].max()])
    plt.scatter(coordinates[:, 0], coordinates[:, 1])  # to plot the sites
    plt.plot(coordinates[:, 0], coordinates[:, 1])  # to plot the paths
    if original_path:
        plt.scatter(coordinates[0, 0], coordinates[0, 1], color='r')  # plot the staring point in red color
        plt.savefig("Plots2/Uoriginal-" + filler)
    elif approx_sol:
        plt.scatter(coordinates[0, 0], coordinates[0, 1], color='r')  # plot the staring point in red color
        plt.savefig("Plots2/approx-" + filler)
    else:
        plt.savefig("Plots2/random-" + filler)
    plt.close()


# Exact Solution

def find_best_route(starting_point, G):
    """
    don't use this.  ~(2^n)*(n^2)
    :param starting_point:
    :param G:
    :return:
    """
    # return list(G.nodes())
    min_path_weight = 99999999  # TODO INFINITY
    best_path = []
    for i in G.nodes():
        if i == starting_point:
            continue
        # calc cost if it is less then save it
        path_weight, path = cost(G, starting_point, G.nodes(), i)
        if path_weight < min_path_weight:
            min_path_weight = path_weight
            best_path = path + [i]
    return [starting_point] + best_path


def cost(G, starting_point, S, i):
    """
    :param G:
    :param starting_point:
    :param S: a set of vertices of the graph excluding the starting point
    :param i: vertex for which the cost is to be calculated
    :return:
    """
    if len(S) <= 2:
        return G[starting_point][i]['weight'], [i]
    # C(S, i) = min { C(S-{i}, j) + dis(j, i)} where j belongs to S, j != i and j != 1.
    temp = S.copy()
    temp.remove(i)
    ci = 999999999  # TODO INFINITY
    min_path = []
    for j in temp:
        if j == starting_point:
            continue
        c, path = cost(G, starting_point, temp, j)
        if c + G[i][j]['weight'] < ci:
            ci = c + G[i][j]['weight']
            min_path = path + [j]
    return ci, min_path


# Approximate solution

def find_approximate_route(starting_point, G):
    curr = starting_point
    visited = [starting_point]
    time = 0
    pt = 0
    while True:
        # finding nearest neighbour
        nn = None
        dist = 9999999  # TODO INFINITY
        for node in G.neighbors(curr):
            if node not in visited:
                if G[curr][node]['weight'] < dist:
                    nn = node
                    dist = G[curr][node]['weight']
        if nn is None:
            break
        else:
            curr = nn
            time += (dist / 40 + 0.5)
            if time > 8:
                print(str(pt) + "," + str(time))
                if time == pt:
                    return visited
                pt = time
                time = 0
                curr = starting_point
            visited += [curr]
    return visited
