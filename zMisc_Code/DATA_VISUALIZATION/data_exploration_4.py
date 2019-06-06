import pandas as pd

# mytable = pd.read_csv("~/Desktop/DTXCIDs_fingerprints_full_v0.tsv" , sep='\t')
#
# # print(mytable.head())
#
# frequencytable = mytable.count(axis=1)
#
# print(frequencytable.shape)
# print(frequencytable.head())
#
# frequencytable = pd.DataFrame(columns=mytable[1:].columns, index=['0','1','wut'])
#
# for col in mytable[1:].columns:
#     try:
#         frequencytable[col]['0'] = (mytable[col].value_counts()[0])
#         frequencytable[col]['1'] = (mytable[col].value_counts()[1])
#     except:
#         print('error', col)
#         pass
#
#     try:
#         frequencytable[col]['wut'] = (mytable[col].value_counts()[2])
#     except:
#         pass
#     # for i in mytable[col].value_counts():
#     #     print(i, mytable[col].value_counts()[i])
#     # print(mytable[col].value_counts()[0].type())
#     # print(mytable[col].value_counts()[2])
#
# frequencytable.to_csv("~/Desktop/frequencytable_toxprints.tsv" , sep='\t', index=False)
# # print(frequencytable.head())

##import frequency table
mytable2 = pd.read_csv("~/Desktop/Toxprint_Frequency/frequencytable_toxprints_v1.tsv" , sep='\t')

# print(mytable2.index)

#graph some shit
import seaborn as sns
import matplotlib.pyplot as plt


g, ax = plt.subplots(figsize=(8,15))
sns.set_context("talk")
# sns.set_color_codes(8)
# a = a[0:25]
# sns.barplot( x = a, y = a.index, palette='GnBu_d')
# ax.set(title= 'Frequency of Toxprints Across All Assays',ylabel='Descriptor\'s Name', xlabel = 'Count')
# plt.show()

#different color schemes
mypalette='GnBu_d'
# mypalette='PiYG'
# mypalette='YlGnBu'
# mypalette='Spectral'

#sort values
mytable2 = mytable2.sort_values(by=[1], axis=1, ascending=False)

xx = mytable2.iloc[:, 0:50]
# xx = mytable2

### vertical bar plot ###

p = sns.barplot( y = xx.columns, x = xx.iloc[1], palette=mypalette)
# p.set(title= 'Top 50 Most Frequently Inactive\nChemotypes Across All Assays', xlabel = 'Percent of Total Assays')
p.set(title= 'Top 50 Most Abundant Toxprints\nAcross All DTXCIDs', xlabel = 'Counts')

# attempt to add values to graph bars
# for index, row in zip(xx.index, xx):
#     p.text(index, row, row, color='black', ha="center")
plt.tight_layout()
plt.show()


### circular barplot ###

# import numpy as np
# import matplotlib.pyplot as plt
#
# N = 50
# bottom = 8
# max_height = 4
#
# theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
# radii = xx.iloc[1]
# width = (2*np.pi) / N
#
# ax = plt.subplot(111, polar=True)
# bars = ax.bar(theta, radii, width=width, bottom=bottom)
#
# # Use custom colors and opacity
# for r, bar in zip(radii, bars):
#     bar.set_facecolor(plt.cm.jet(r / 10.))
#     bar.set_alpha(0.8)
#
# plt.show()

