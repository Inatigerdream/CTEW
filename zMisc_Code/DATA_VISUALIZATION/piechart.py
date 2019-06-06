import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from random import sample

# create a shuffled seaborn color palette
b = sample(sns.color_palette('coolwarm', 7), 7)
sns.palplot(sample(sns.color_palette('coolwarm', 7), 7))

# make a donut plot

def piechart(data, labels, title='', save=''):
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    tot = sum(data)

    wedges, texts = ax.pie(data, wedgeprops=dict(width=0.4), startangle=-90 , colors=b)#['#f9dc26', '#F27059', '#b497d6', '#8be0f6', '#eafbfa']) #['#0e7c7b', '#d62246', '#3D348B', '#D8E4FF',  '#17bebb'] )

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate('{} ({}) {}%'.format(labels[i], data[i], round((data[i]/tot)*100, 1)), xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                     horizontalalignment=horizontalalignment, **kw)

    ax.set_title(title, backgroundcolor='white')
    # plt.viridis()
    if save == '':
        plt.show()
    else:
        fig.set_size_inches(15, 7)
        plt.savefig(save, dpi=500, quality=95, format='jpg', orientation='landscape')



# recipe = ["225 g flour",
#           "90 g sugar",
#           "1 egg",
#           "60 g butter",
#           "100 ml milk",
#           "1/2 package of yeast"]

# data = [225, 90, 50, 60, 100, 5]


# import assay category data
import pandas as pd
cats = pd.read_csv('/home/rlougee/Desktop/primary_data/categories_table_invitrodb_v2.tsv', sep='\t')
for x in cats.columns[2:]:
    cats2 = cats[x].value_counts()
    piechart(cats2, cats2.index, "Assay_Category:{}".format(" ".join((x.split('_'))).title()))