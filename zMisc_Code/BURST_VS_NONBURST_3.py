import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from PullEnrichment.ImageMaker import imagemaker

# import burst and nonburst results
burst = pd.read_csv('/home/rlougee/Desktop/primary_data/burst.tsv', sep='\t')
nonburst = pd.read_csv('/home/rlougee/Desktop/primary_data/nonburst.tsv', sep='\t')

# import "cytoxicity" categories (mitochondiral disruption, oxidative stress, etc)
cytox = pd.read_excel('/home/rlougee/Desktop/primary_data/toxsci-15-0719-File010.xlsx')

# remove extra columns
cytox = cytox[['assay', 'aeid', 'biological_process']]

burst_full = pd.merge(cytox, burst, how='right', left_on='assay', right_on='name')
nonburst_full = pd.merge(cytox, nonburst, how='right', left_on='assay', right_on='name')

# print(cytox.shape, burst.shape, burst_full.shape, nonburst.shape, nonburst_full.shape)
# print(burst_full)
# burst_full.to_csv('/home/rlougee/Desktop/burst_full.tsv', sep='\t')

# # look at specific biological_process categories
print(cytox['biological_process'].unique())
# print(burst_full.loc[burst_full['biological_process'].isin(['oxidative stress up'])])

mylist = ['oxidative stress up']

burst_plot = burst_full.loc[burst_full['biological_process'].isin(mylist)]
nonburst_plot = nonburst_full.loc[nonburst_full['biological_process'].isin(mylist)]

print(burst_plot.shape, nonburst_plot.shape)


# start making plots
# get value counts for b v nb
burst_VC = burst_plot['descriptors_name'].value_counts()
nonburst_VC = nonburst_plot['descriptors_name'].value_counts()
# full_VC = pd.merge( pd.DataFrame(nonburst_VC), pd.DataFrame(burst_VC), left_index=True, right_index=True)
full_VC = pd.merge(pd.DataFrame(nonburst_VC), pd.DataFrame(burst_VC), how='outer', left_index=True, right_index=True)
full_VC = full_VC.fillna(value=0).sort_values(by=['descriptors_name_x', 'descriptors_name_y'], axis=0, ascending=False)


# double bar plot for this?
barwidth = 0.3
n = 500
r1 = np.arange(len(full_VC['descriptors_name_x'][:n]))
r2 = [x + barwidth for x in r1]

fig, ax = plt.subplots()

rects1 = ax.bar(r1, full_VC['descriptors_name_x'][:n], barwidth, color='turquoise', alpha=1, zorder=3, label='Non-Burst Filtered')
rects2 = ax.bar(r2, full_VC['descriptors_name_y'][:n], barwidth, color='dodgerblue', alpha=.8, zorder=3, label='Burst Filtered')

# add labels
ax.set_ylabel('Counts', fontsize=14, fontweight='bold')
ax.set_title('Frequency of Burst and Non-Burst Significant Chemotypes in {} Assays'.format(mylist[0]), fontsize=14, fontweight='bold')
ax.set_xticks(r1)
ax.set_xticklabels(full_VC.index[:n+1], rotation='vertical', fontweight='bold')
ax.set_facecolor('.98')
ax.grid(color='.9', zorder=0)
ax.legend()

# auto label
def autolabel(rects, xpos='center'):
    """
    attach a text label above each bar displaying its height
    """
    xpos = xpos.lower() # normalize in case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                '{}'.format(int(height)), ha=ha[xpos], va='bottom')

autolabel(rects1, "center")
autolabel(rects2, "center")

# plt.tight_layout()

print(full_VC, len(full_VC.index))
plt.show()

# imagemaker(pd.DataFrame(full_VC.index, columns=['Chemotype ID']), mylist[0],'/home/rlougee/Desktop/figures_ACS_2/Cytotoxicity_category_pics/')