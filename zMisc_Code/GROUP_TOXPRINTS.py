import pandas as pd
import glob
import sys
import re

# # # THIS PROGRAM IS FOR SHOWING GROUPS OF ENRICHED CHEMOTYPES # # #
# you should input a list of enriched chemotypes and it will return a file containing group statistics
cats1 = pd.read_excel('/home/rlougee/Desktop/GROUP_TXP/TXP_5levels.xlsx')
cats2 = pd.read_excel('/home/rlougee/Desktop/GROUP_TXP/ToxPrintAllSubsets.xlsx')

#format
cats1 = cats1.drop(['ToxPrint_ID'], axis=1)
cats2 = cats2.drop(['TP_sort', 'TP_ID'], axis=1)
txplist = ["Txp-" + str(x) for x in range(1, 730)]
cats1.insert(0, 'Toxprint_ID', txplist)
cats2['Toxprint_ID'] = txplist
cats = pd.merge(cats1, cats2, on='Toxprint_ID')
cats.insert(1, 'Toxprint_Name', cats['ToxPrint_chemotype_name (original)'])
cats = cats.drop(['ToxPrint_729', 'ToxPrint_chemotype_name (original)' ], axis=1)

# print(cats.head())



# write a dict to store all the groups
LD = {}

# Toxprint Level 1
L1 = cats['Level 1'].unique()
print('\nLEVEL 1', len(L1), L1)
for i in L1:
    LD[i] = cats.loc[cats['Level 1'] == i]['Toxprint_ID']

# Toxprint Level 2
L2 = cats['Level 2'].unique()
print('\nLEVEL 2', len(L2))
for i in L2:
    LD[i] = cats.loc[cats['Level 2'] == i]['Toxprint_ID']

# # Toxprint Level 3
L3 = cats['Level 3'].unique()
print('\nLEVEL 3', len(L3))
# for i in L3:
#     print(i, len(cats.loc[cats['Level 3'] == i]))
#
# # Toxprint Level 4
L4 = cats['Level 4'].unique()
print('\nLEVEL 4', len(L4))
# for i in L4:
#     print(i, len(cats.loc[cats['Level 4'] == i]))
#
# # Toxprint Level 5?
L5 = cats['Level 5'].unique()
print('\nLEVEL 5', len(L5))

# for i in L5:
#     print(i, len(cats.loc[cats['Level 5'] == i]))

# TTC alerts
LD['TTC_Alerts'] = cats.loc[cats['ToxPrint_74TTC'] == 1]['Toxprint_ID']
print('\nTTC alerts', len(LD['TTC_Alerts']))


# Ashby alerts
LD['Ashby_Alerts'] = cats.loc[cats['ToxPrint_33Ashby'] == 1]['Toxprint_ID']
print('\nAshby Alerts', len(LD['Ashby_Alerts']))

# Toxprint 60??
LD['TXP60'] = cats.loc[cats['ToxPrint_60Profiling'] == 1]['Toxprint_ID']
print('\nToxPrint_60Profiling', len(LD['TXP60']))


sys.exit(0)


# remove really small categories
# maybe should remove others?
delist = []
for i in LD:
    if len(LD[i]) == 1:
        # print(i)
        delist.append(i)

for i in delist:
    del LD[i]

# # # DICTIONARY OF CATEGORIES IS COMPLETE # # #
# now add files and output groups that have many chemotypes

# a = pd.read_csv('/home/rlougee/Desktop/GROUP_TXP/Assay_Cat_Enrichment_Tables/analysis_direction_negative_table.tsv', sep='\t')

big_dict = {}

for f in glob.glob('/home/rlougee/Desktop/GROUP_TXP/Assay_Cat_Enrichment_Tables/*'):
    a = pd.read_csv(f, sep='\t')

# for i in LD:
#     print(LD[i] in a['Fingerprint_ID'])
    for i in LD:
        bla = [x for x in a["Fingerprint_ID"] if x in list(LD[i])]
        if len(bla)/len(LD[i])*100 > 30:
            big_dict[f.split("/")[-1].split("_table")[0]] = [ i, round(len(bla)/len(LD[i])*100, 0), len(bla), len(LD[i]), list(LD[i])]

bla = pd.DataFrame.from_dict(big_dict, orient='index')
bla.columns = [ 'Toxprint_Group', 'Percent_Enriched', 'Total_Enriched', 'Total_in_Group', "Txp_list"]
bla.to_csv('/home/rlougee/Desktop/TXP_groups_for_all_Assay_Cats2.tsv', sep='\t')