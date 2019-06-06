import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

burst = pd.read_csv('/home/rlougee/Desktop/primary_data/burst.tsv', sep='\t')
nonburst = pd.read_csv('/home/rlougee/Desktop/primary_data/nonburst.tsv', sep='\t')


burst_VC = burst['descriptors_name'].value_counts()
nonburst_VC = nonburst['descriptors_name'].value_counts()
# full_VC = pd.merge(pd.DataFrame(burst_VC), pd.DataFrame(nonburst_VC), left_index=True, right_index=True) # reverse flip labels and colors
full_VC = pd.merge( pd.DataFrame(nonburst_VC), pd.DataFrame(burst_VC), left_index=True, right_index=True)
# full_VC = pd.merge( pd.DataFrame(burst_VC), pd.DataFrame(nonburst_VC), how='outer', left_index=True, right_index=True)
full_VC = full_VC.fillna(value=0).sort_values(by=['descriptors_name_x', 'descriptors_name_y'], axis=0, ascending=False)

# double bar plot for this?
barwidth = 0.3
n = 200
r1 = np.arange(len(full_VC['descriptors_name_x'][:n]))
r2 = [x + barwidth for x in r1]

fig, ax = plt.subplots()

rects1 = ax.bar(r1, full_VC['descriptors_name_x'][:n], barwidth, color='turquoise', alpha=1, zorder=3, label='Non-Burst Filtered')
rects2 = ax.bar(r2, full_VC['descriptors_name_y'][:n], barwidth, color='magenta', alpha=.8, zorder=3, label='Burst Filtered')

# add labels
ax.set_ylabel('Count of Enriched Assays', fontsize=14, fontweight='bold')
ax.set_xlabel('Toxprint Chemotypes', fontsize=14, fontweight='bold')
ax.set_title('Frequency of Burst and Non-Burst Significant Chemotypes', fontsize=24, fontweight='bold')
ax.set_xticks([0, 200])
# ax.set_xticklabels(full_VC.index[:n+1], rotation='vertical', fontweight='bold')
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

# autolabel(rects1, "center")
# autolabel(rects2, "center")

# plt.tight_layout()
plt.show()

full_VC.to_csv('/home/rlougee/Desktop/poop.csv')