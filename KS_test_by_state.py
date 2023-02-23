#
# POI_statistics = r'D:\Siqin Wang\U.S rest project_updated\POI_information\Join192021_2022version.csv'
# df_data = pd.read_csv(POI_statistics)
# df_data = df_data.groupby('placekey').mean()


import csv
import os
import json
from scipy import stats
import numpy as np
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import read_csv
import pandas as pd
from scipy import stats
import statistics
from scipy.stats import gaussian_kde
from scipy.stats import ttest_ind

FIPS_StateABBR_dic = {
	"1" : "AL",
    "2" : "AK",
	"4" : "AZ",
	"5" : "AR",
	"6" : "CA",
	"8" : "CO",
	"9" : "CT",
    "10": "DE",
    "11": "DC",
    "12": "FL",
    "13": "GA",
    "15": "HI",
    "16": "ID",
    "17": "IL",
    "18": "IN",
    "19": "IA",
    "20": "KS",
    "21": "KY",
    "22": "LA",
    "23": "ME",
    "24": "MD",
    "25": "MA",
    "26": "MI",
    "27": "MN",
    "28": "MS",
    "29": "MO",
    "30": "MT",
    "31": "NE",
    "32": "NV",
    "33": "NH",
    "34": "NJ",
    "35": "NM",
    "36": "NY",
    "37": "NC",
    "38": "ND",
    "39": "OH",
    "40": "OK",
    "41": "OR",
    "42": "PA",
    "44": "RI",
    "45": "SC",
    "46": "SD",
    "47": "TN",
    "48": "TX",
    "49": "UT",
    "50": "VT",
    "51": "VA",
    "53": "WA",
    "54": "WV",
    "55": "WI",
    "56": "WY",
	}

def retrieve_list_of_variables_for_a_certain_state (statename):
    POI_path = r'D:\Siqin Wang\U.S rest project_updated\POI_information\Join192021_2022version_yearly.csv'
    visit19_list = []
    visit20_list = []
    visit21_list = []
    revenue19_list = []
    revenue20_list = []
    revenue21_list = []

    Ratio_Lvisit1920_list = []
    Ratio_Lvisit1921_list = []
    Ratio_Lrevenu1920_list = []
    Ratio_Lrevenu1921_list = []
    Ratio_LrevenuTotal_list = []



    with open(POI_path) as f:
        readerf = csv.reader(f)
        next(readerf)
        for row in readerf:
            if float(row[6]) > 30 and float(row[7]) > 30 and float(row[8]) > 30 and POI_statename_dict[row[0]]== statename and float(row[12]) < 1 and float(row[13]) < 1:
                visit19 = float(row[6])
                visit20 = float(row[7])
                visit21 = float(row[8])
                revenue19 = float(row[9])
                revenue20 = float(row[10])
                revenue21 = float(row[11])

                Ratio_Lvisit1920 = float(row[12])
                Ratio_Lvisit1921 = float(row[13])
                Ratio_Lrevenu1920 = float(row[14])
                Ratio_Lrevenu1921 = float(row[15])
                Ratio_LrevenuTotal = float(row[16])

                visit19_list.append(visit19)
                visit20_list.append(visit20)
                visit21_list.append(visit21)
                revenue19_list.append(revenue19)
                revenue20_list.append(revenue20)
                revenue21_list.append(revenue21)

                Ratio_Lvisit1920_list.append(Ratio_Lvisit1920)
                Ratio_Lvisit1921_list.append(Ratio_Lvisit1921)
                Ratio_Lrevenu1920_list.append(Ratio_Lrevenu1920)
                Ratio_Lrevenu1921_list.append(Ratio_Lrevenu1921)
                Ratio_LrevenuTotal_list.append(Ratio_LrevenuTotal)

    Ratio_Lvisit19_20AND21_list = np.average(np.array([Ratio_Lvisit1920_list, Ratio_Lvisit1921_list]),axis=0).tolist()

    Ratio_Lrevenu19_20AND21_list = np.average(np.array([Ratio_Lrevenu1920_list, Ratio_Lrevenu1921_list]), axis=0).tolist()

    #return choices:
    # Ratio_Lvisit1920_list
    # Ratio_Lvisit1921_list
    # Ratio_Lrevenu1920_list
    # Ratio_Lrevenu1921_list
    # Ratio_LrevenuTotal_list
    # Ratio_Lvisit19_20AND21_list
    # Ratio_Lrevenu19_20AND21_list

    return Ratio_Lrevenu19_20AND21_list



# construct POI_State_dict
POI_monthly = r'D:\Siqin Wang\U.S rest project_updated\POI_information\Join192021_2022version.csv'
POI_statename_dict = {}
restaurant_statename_list = []
with open(POI_monthly) as f:
  readerf = csv.reader(f)
  next(readerf)
  for row in readerf:
      POIID = row[0]
      stateID = row[8]
      statename = FIPS_StateABBR_dic[stateID]

      POI_statename_dict[POIID] = statename

      if statename not in restaurant_statename_list:
          restaurant_statename_list.append(statename)

print (len(restaurant_statename_list))
print (restaurant_statename_list)

restaurant_statename_list = ['WA', 'CA', 'GA']

rest_sequence = dict(zip(restaurant_statename_list, list(range(len(restaurant_statename_list)))))
rows, cols = (len(restaurant_statename_list), len(restaurant_statename_list))

arr_ks = [[0.0]*cols]*rows
arr_ks = np.asarray(arr_ks)

arr_p = [[0.0]*cols]*rows
arr_p = np.asarray(arr_p)


combinations = [(a, b) for idx, a in enumerate(restaurant_statename_list) for b in restaurant_statename_list[idx + 1:]]

for combination in combinations:

    ks_distance, p = stats.ks_2samp(retrieve_list_of_variables_for_a_certain_state(combination[0]), retrieve_list_of_variables_for_a_certain_state(combination[1]))
    arr_ks[rest_sequence[combination[0]]][rest_sequence[combination[1]]] = ks_distance
    arr_ks[rest_sequence[combination[0]]][rest_sequence[combination[0]]] = 0.0
    arr_ks[rest_sequence[combination[1]]][rest_sequence[combination[0]]] = ks_distance

    arr_p[rest_sequence[combination[0]]][rest_sequence[combination[1]]] = p
    arr_p[rest_sequence[combination[0]]][rest_sequence[combination[0]]] = 10
    arr_p[rest_sequence[combination[1]]][rest_sequence[combination[0]]] = p

    #t_stat, p = ttest_ind(retrieve_list_of_variables_for_a_certain_type(combination[0]), retrieve_list_of_variables_for_a_certain_type(combination[1]))
    # arr_ks[rest_sequence[combination[0]]][rest_sequence[combination[1]]] = t_stat
    # arr_ks[rest_sequence[combination[0]]][rest_sequence[combination[0]]] = t_stat
    # arr_ks[rest_sequence[combination[1]]][rest_sequence[combination[0]]] = t_stat

    # arr_p[rest_sequence[combination[0]]][rest_sequence[combination[1]]] = p
    # arr_p[rest_sequence[combination[0]]][rest_sequence[combination[0]]] = p
    # arr_p[rest_sequence[combination[1]]][rest_sequence[combination[0]]] = p


    #print (ks_distance)
    print (rest_sequence[combination[0]], rest_sequence[combination[1]])


    #arr_p[rest_sequence[combination[0]]][rest_sequence[combination[1]]] = p

    print (combination)
    print (arr_ks)


df_arr_ks = pd.DataFrame(arr_ks)
df_arr_ks.columns = restaurant_statename_list
df_arr_ks.index = restaurant_statename_list

g = sns.clustermap(df_arr_ks, fmt='.2f', cbar_kws={"shrink": 1.5}, linecolor='white', method="single", linewidths=0.3, cmap = 'OrRd', cbar_pos=(.91, .2, .02, .6), yticklabels=1, xticklabels=1)
g.ax_heatmap.set_position([0.1, 0.1, 0.8, 0.8])

g.ax_heatmap.yaxis.set_ticks_position("left")

g.ax_row_dendrogram.remove()
g.ax_col_dendrogram.remove()


#plt.setp(g.ax_heatmap.get_xticklabels(), horizontalalignment='right', rotation=45) # For x axis
#plt.setp(g.ax_heatmap.get_yticklabels(), horizontalalignment='left', rotation=45) # For x axis
for i, ix in enumerate(g.dendrogram_row.reordered_ind):
    for j, jx in enumerate(g.dendrogram_row.reordered_ind):
        if i != j:
            text = g.ax_heatmap.text(
                j + 0.5,
                i + 0.5,
                "***" if (arr_p[ix, jx] <0.001 or arr_p[jx, ix]<0.001)
                else "**" if ((arr_p[ix, jx] > 0.001 and arr_p[ix, jx] < 0.01) or (arr_p[jx, ix] > 0.001 and arr_p[jx, ix] < 0.01))
                else '*' if ((arr_p[ix, jx] > 0.01 and arr_p[ix, jx] < 0.1) or (arr_p[jx, ix] > 0.01 and arr_p[jx, ix] < 0.1))
                else '',

                ha="center",
                va="center",
                color="black",
            )
            text.set_fontsize(6)


plt.show()