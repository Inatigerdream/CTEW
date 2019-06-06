import matplotlib.pyplot as plt
import pandas as pd

from zMisc_Code.DATA_VISUALIZATION.sunburst import sunburst

cats1 = pd.read_excel('/home/rlougee/Desktop/GROUP_TXP/TXP_5levels.xlsx')

cats1 = cats1.drop(['ToxPrint_ID'], axis=1)
txplist = ["Txp-" + str(x) for x in range(1, 730)]
cats1.insert(0, 'Toxprint_ID', txplist)

# data = [('', 729, [(x, len(cats1.loc[cats1['Level 1'] == x]), [(y, len(cats1.loc[cats1['Level 2'] == y]), [(z, len(cats1.loc[cats1['Level 3'] == z]), []) for z in list(set(cats1.loc[cats1['Level 2'] == y]['Level 3']))]) for y in list(set(cats1.loc[cats1['Level 1'] == x]['Level 2']))]) for x in cats1['Level 1'].unique()
# ]
#          )]

data2 = [('All Txp', 729, [(x, len(cats1.loc[cats1['Level 1'] == x]), [(y, len(cats1.loc[cats1['Level 2'] == y]), []) for y in list(set(cats1.loc[cats1['Level 1'] == x]['Level 2']))]) for x in cats1['Level 1'].unique()
]
         )]




# cats.loc[cats['Level 1'] == i]

sunburst(data2)
plt.show()