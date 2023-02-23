import csv
import os
import json
from scipy import stats
import numpy as np
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

def correct_orgin_cbg_id(origin_id):
  if len(origin_id) == 11:
    corrected_id = '0' + origin_id

  else:
    corrected_id = origin_id
  return corrected_id

def transpose(l1, l2):
  for i in range(len(l1[0])):
    row = []
    for item in l1:
      row.append(item[i])
    l2.append(row)
    print(i)
  return l2

def entropy(labels, base=None):
  value,counts = np.unique(labels, return_counts=True)
  return stats.entropy(counts, base=base)

def attach_labels_according_to_percentile_threshold_list(value, percentile_threshold_list):
  count = 1
  label = percentage_inteval_num
  for threshold in percentile_threshold_list:
    if value > threshold:
      count = count + 1
    else:
      label = count
  return label

#construct MSA_cbg_ID_dictionary
cbg_statistics_path = r'D:\Siqin Wang\U.S rest project_updated\CBG_statistics\SelectedVariableandCentroid_CBG.csv'
MSA_cbg_ID_dic = {}
with open(cbg_statistics_path, encoding="utf8") as f:
  readerf = csv.reader(f)
  next(readerf)
  for row in readerf:
    if row[15] == '1':
      MSA_name = row[14].split(',')[0]
      if (MSA_name not in MSA_cbg_ID_dic):
        MSA_cbg_ID_dic[MSA_name] = [correct_orgin_cbg_id(row[1])]
      else:
        MSA_cbg_ID_dic[MSA_name].append(correct_orgin_cbg_id(row[1]))

#construct poiID_MSA_dictionary
Placekey_State_MSA_path = r'D:\Siqin Wang\U.S rest project_updated\Placekey_State_MSA\Placekey_State_MSA.csv'
poiID_MSA_dict = {}
with open(Placekey_State_MSA_path) as f:
  readerf = csv.reader(f)
  next(readerf)
  for row in readerf:
    poiID = row[0]
    MSA = row[4].split(',')[0]
    poiID_MSA_dict[poiID] = MSA
print (poiID_MSA_dict)

MSA_pct_lowhhincome_dic = {}
MSA_pct_nonwhite_dic = {}

with open(cbg_statistics_path, encoding="utf8") as f:
  readerf = csv.reader(f)
  next(readerf)
  for row in readerf:
    if row[15] == '1':
      MSA_name = row[14].split(',')[0]

      if row[5]!='0':
        if (MSA_name not in MSA_pct_lowhhincome_dic):
          MSA_pct_lowhhincome_dic[MSA_name] = [float(row[6]) / float(row[5])]
        else:
          MSA_pct_lowhhincome_dic[MSA_name].append(float(row[6]) / float(row[5]))

      if row[7]!='0':
        if MSA_name not in MSA_pct_nonwhite_dic and float(row[7])!= 0:
          MSA_pct_nonwhite_dic[MSA_name] = [float(row[10]) / float(row[7])]
        else:
          MSA_pct_nonwhite_dic[MSA_name].append(float(row[10]) / float(row[7]))


percentage_inteval_num = 5
incremental = 100 / percentage_inteval_num

# create interval list for each MSA in terms of lowhhincome and nonwhite
MSA_pct_lowhhincome_interval_dic = {}
for key in MSA_pct_lowhhincome_dic:
    interval_list = []
    for i in range(1, percentage_inteval_num):
      interval_list.append(np.percentile(MSA_pct_lowhhincome_dic[key],i*incremental))
    MSA_pct_lowhhincome_interval_dic[key] = interval_list

MSA_pct_nonwhite_interval_dic = {}
for key in MSA_pct_nonwhite_dic:
    interval_list = []
    for i in range(1, percentage_inteval_num):
      interval_list.append(np.percentile(MSA_pct_nonwhite_dic[key],i*incremental))
    MSA_pct_nonwhite_interval_dic[key] = interval_list

#construct cbgID_nonwhitepct_dict; cbgID_lowincomepct_dict
cbgID_lowhhincomePct_dic = {}
cbgID_nonwhitePct_dic = {}

with open(cbg_statistics_path, encoding="utf8") as f:
  readerf = csv.reader(f)
  next(readerf)
  for row in readerf:
    cbgID = correct_orgin_cbg_id(row[1])
    if row[5] != '0':
      cbgID_lowhhincomePct_dic[cbgID] = float(row[6]) / float(row[5])

    if row[7] != '0':
      cbgID_nonwhitePct_dic[cbgID] = float(row[10]) / float(row[7])


with open(r'D:\Siqin Wang\U.S rest project_updated\poiIDMonth_cbgIDlist_dict.pickle', 'rb') as handle:
  poiIDMonth_cbgIDlist_dict = pickle.load(handle)
count = 0

writepath = r'D:\Siqin Wang\U.S rest project_updated\POI_monthly_entropy\POI_monthly_entropy_for_poi_in_MSA_and_travel_within_that_MSA.csv'

with open(writepath, 'w', newline='') as csvfile:
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(["poiID", "month", "MSA", "lowhhincomePct_entropy", 'nonwhitePct_entropy', 'lowhhincomePct_labelSize',
                      'nonwhitePct_labelSize'])

  for poiIDMonth in poiIDMonth_cbgIDlist_dict:
    try:
      poiID = poiIDMonth.split('*')[0]
      MSA = poiID_MSA_dict[poiID]

      if MSA != "nonMSA":
        cbg_list_within_this_MSA = MSA_cbg_ID_dic[MSA]

        lowhhincomePct_list = []
        nonwhitePct_list = []
        for origin_cbgID in poiIDMonth_cbgIDlist_dict[poiIDMonth]:
          if origin_cbgID in cbg_list_within_this_MSA:
            lowhhincomePct = cbgID_lowhhincomePct_dic[origin_cbgID]
            lowhhincomePct_list.append(lowhhincomePct)
            nonwhitePct = cbgID_nonwhitePct_dic[origin_cbgID]
            nonwhitePct_list.append(nonwhitePct)

        #calculate normalized lowhhincomePct entropy
        lowhhincomePct_label_list = []
        for lowhhincomePct in lowhhincomePct_list:
          lowhhincomePct_label_list.append(attach_labels_according_to_percentile_threshold_list(lowhhincomePct, MSA_pct_lowhhincome_interval_dic[MSA]))
        lowhhincomePct_entropy = entropy(lowhhincomePct_label_list)/np.log(len(lowhhincomePct_label_list))

        nonwhitePct_label_list = []
        for nonwhitePct in nonwhitePct_list:
          nonwhitePct_label_list.append(attach_labels_according_to_percentile_threshold_list(nonwhitePct, MSA_pct_nonwhite_interval_dic[MSA]))
        nonwhitePct_entropy = entropy(nonwhitePct_label_list)/np.log(len(nonwhitePct_label_list))

        writerow = [poiIDMonth.split('*')[0],poiIDMonth.split('*')[1],MSA,lowhhincomePct_entropy, nonwhitePct_entropy, len(lowhhincomePct_label_list), len(nonwhitePct_label_list)]
        csvwriter.writerow(writerow)
        #writerows.append(writerow)
        #print (writerow)


        count = count + 1
        if count %10000 == 0:
          print (count)


    except:
      pass

# with open(writepath, 'w', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(["poiID", "month", "lowhhincomePct_entropy", 'nonwhitePct_entropy', 'lowhhincomePct_labelSize', 'nonwhitePct_labelSize'])
#     csvwriter.writerows(writerows)


