import pandas as pd
import re
from GraphProcessing import *

# F = filler, F_LAT = Filler Latitude, F_LONG = Filler Longitude, S_LAT = Site Latitude, S_LONG = Site Longitude
data = pd.read_csv(r"FuelFiller.csv")

site_coordinates = pd.read_csv(r"SiteLoc.csv")
site_coordinates.drop_duplicates(inplace=True)

data.sort_values(by="F")
fillers = data["F"].unique()  # list of all the fillers

file = open("pathWeights2.txt", mode='w')
file.write("filler - wt, uwt, owt" + "\n")

for filler in fillers:
    if filler == "Dummy Filler -1223454545":
        continue

    # getting a list of sites for the current filler and the weights of the default path taken
    sites_to_visit = data[data["F"] == filler]
    filler = re.sub("[^A-Za-z]+", "", filler)
    sites = []
    wt = 0  # weight of the default path
    uwt = 0  # weight of the unique site default path
    flag = False
    time = 0  #
    pt = 0  #
    for idx, row in sites_to_visit.iterrows():
        if flag:
            a = site_coordinates.loc[site_coordinates["S_ID"] == site].values[0]
        site = site_coordinates.loc[
            (site_coordinates["LATITUDE"] == row["S_LAT"]) & (site_coordinates["LONGITUDE"] == row["S_LONG"])][
            "S_ID"].max()
        if not flag:
            starting_point = site_coordinates.loc[site_coordinates["S_ID"] == site].values[0]  #
        if flag:
            b = site_coordinates.loc[site_coordinates["S_ID"] == site].values[0]
            w = geographical_distance((a[1], a[2]), (b[1], b[2]))
            time += (w / 40 + 0.5)
            if time > 8:
                wt += geographical_distance((starting_point[1], starting_point[2]), (b[1], b[2]))
                wt += geographical_distance((starting_point[1], starting_point[2]), (a[1], a[2]))
                if time == pt:
                    break
            wt += w
        if site not in sites:
            if flag:
                uwt += w
            sites.append(site)
        flag = True

    # current_loc = (sites_to_visit.loc[0]["S_LAT"], sites_to_visit.loc[0]["S_LONG"])
    # current_loc = "ASMO_0203"  # TODO what should be the starting location

    print(filler)

    # plotting the default route
    plot_route(sites, filler, site_coordinates, original_path=True)

    # plotting the calculated optimal route
    route = best_route(sites, site_coordinates, approx_sol=True)
    plot_route(route, filler, site_coordinates, approx_sol=True)

    owt = 0  # weight of the optimal path
    for i in range(len(route) - 1):
        a = site_coordinates.loc[site_coordinates["S_ID"] == route[i]].values[0]
        b = site_coordinates.loc[site_coordinates["S_ID"] == route[i + 1]].values[0]
        w = geographical_distance((a[1], a[2]), (b[1], b[2]))
        owt += w

    file.write(filler + "(" + str(len(sites)) + "," + str(len(sites_to_visit)) + ")" + "- " + str(wt) + ","
               + str(uwt) + "," + str(owt) + "\n")
