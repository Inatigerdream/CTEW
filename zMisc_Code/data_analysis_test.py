import pandas as pd
from ggplot import *
import seaborn as sns

#
#

mytable2 = pd.read_csv('~/Desktop/FULL_TP_ENRICHMENTS.tsv', sep='\t')



# for i in range(0,1000,5):

blabla = mytable2.truncate(before=90, after=111)
# g = ggplot(aes( x='OR'), data=blabla) + geom_density()
#
#
# #     + theme(
# #
# #     plot_title = element_text('Odd\'s Ratios', size=33, vjust=-.05),
# #     axis_title_x = element_text('Descriptor\'s Name',size=22, vjust = -.035),
# #     axis_title_y = element_text('Odd\'s Ratio', size=22),
# #     axis_text_x = blabla['descriptors_name'].all()
# #
# # )
# print(blabla.dtypes)
# print(g)
# # print(blabla.head())
# # print(g)

########################################################################################################################
#seaborn code

import matplotlib.pyplot as plt

# sns.set(style='white')
sns.set_style("darkgrid", {"axes.facecolor": "4.9"})
sns.set_context("talk")#, font_scale=1.11, rc={"grid.color":"blue"})
gg =sns.factorplot(x='descriptors_name',y='P-Val', kind='bar', data=blabla, palette='GnBu_d', size=6, aspect=1.5)
gg.set_xticklabels(rotation=70)
gg.set(title= 'P-Values for Toxprints',xlabel='Descriptor\'s Name', ylabel = 'P-Value')
# rc={'font.size':40}
# gg.set_context("poster", rc={"axes.titlesize":8})
# gg.axes.set_title('P-Values for Toxprints', fontsize=50)
# gg.axes.facecolor('dark')
# gg.axes_style()

plt.show()