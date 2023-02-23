import csv
import textdistance
import numpy as np

from random import choices


population = [2, 3, 4]
weights = [0.724, 0.197, 0.079]

print (choices(population, weights))


path = r'D:\Siqin Wang\U.S rest project_updated\Raw_CBG_data\modified_cbg_monthly_od_2019_2021_June.csv'
full_write_path = r'D:\Siqin Wang\U.S rest project_updated\Disaggregated_CBG_data\modified_cbg_monthly_od_2019_2021_June.csv'

count = 0

with open(full_write_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['placekey', 'visitation', 'month', 'year', 'cbg', 'tract', 'county', 'state'])

    with open(path) as f:
        readerf = csv.reader(f)
        #next(readerf)
        for row in readerf:
            #print (row)
            placekey = row[0].split('\t') [0]
            cbg = row[0].split('\t') [1]
            visitation = row[0].split('\t') [2]
            year = row[0].split('\t') [3]
            month = row[0].split('\t') [4]

            if visitation == '4':
                updated_visitation = choices(population, weights)[0]
            else:
                updated_visitation = visitation

            state = cbg[:2]
            county = cbg[:5]
            tract = cbg[:11]
            #print (cbg,state, county,tract)
            writerow = [placekey,updated_visitation,month,year, cbg,tract,county, state]

            csvwriter.writerow(writerow)

            count = count + 1
            if count %1000000 ==0:
                print(count)
