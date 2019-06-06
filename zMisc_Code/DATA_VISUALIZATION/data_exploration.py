import pandas as pd
from ggplot import *
import seaborn as sns

### import data ###

#toxprints only
mytable2 = pd.read_csv('~/Desktop/DUMP_5-15-2018/FULL_TP_ENRICHMENTS.tsv', sep='\t')

# all CTs
# mytable2 = pd.read_csv('~/Desktop/complete_enrichment_data.tsv', sep='\t')

#get total assays
total_assay = len(mytable2['assay_component_endpoint_name'].unique())

#table info
print(mytable2.columns)


#get subsets of data
# werkintable = mytable2[(mytable2['OR']>3)]
werkintable = mytable2[(mytable2['P-Val']<.05) & (mytable2['OR']>3)]
# werkintable2 = mytable2[(mytable2['Inv OR']>3)]
werkintable2 = mytable2[(mytable2['Inv P-val']<0.05) & (mytable2['Inv OR']>3)]

#how many rows were dropped?
print(mytable2.shape)
print(werkintable.shape)
print(werkintable2.shape)

#frequency of significant toxprints / assays
a = werkintable['descriptors_name'].value_counts()
b = werkintable['label'].value_counts()
c = werkintable['assay_component_endpoint_name'].value_counts()

#frequency of insignificant toxprints /assays
d = werkintable2['descriptors_name'].value_counts()
e = werkintable2['label'].value_counts()
f = werkintable2['assay_component_endpoint_name'].value_counts()

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

xx = b[:20]

p = sns.barplot( x = xx/17.76, y = xx.index, palette=mypalette)
p.set(title= 'Top 20 Most Frequently Active\nToxprints Across All Assays', xlabel = 'Percent of Total Assays')
# p.set(title= 'Top 50 Assays with High\nPercentage of Active Chemotypes', xlabel = 'Percent of Total Chemotypes')

# attempt to add values to graph bars
# for index, row in zip(xx.index, xx):
#     p.text(index, row, row, color='black', ha="center")
plt.tight_layout()
plt.show()

print(len(xx.index))
print(xx.index)

# #save figure
# fig = p.get_figure()
# fig.savefig("/share/home/rlougee/Desktop/proj_images/t20_prom_Assays_TP(Inv).png")