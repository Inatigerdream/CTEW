import matplotlib.pyplot as plt
import pandas as pd

from database.database_schemas import Schemas
from database.qsar.descriptors import Descriptors
from database.session import SQLSession

# # # LETS MAKE A RADAR PLOT # # #
# need data

wow = pd.read_csv("/home/rlougee/Desktop/ALL_AEID_ENRICHMENT_DATA.tsv", sep='\t')
wowie = wow[['name','descriptors_name','OR']]

# print(wow.head())

for i in wowie['name'].unique():
    bla = wowie[wowie['name'] == i]
    blabla = pd.DataFrame(bla.iloc[:,1:])
    print(blabla.head(), blabla.shape)

    # for idx, row in blabla.iterrows():
        # if row[1] >= 40:
        #     # print(row[1])
        #     blabla.iloc[idx, 1] = 10
        #     # print(blabla.iloc[idx,1])


    # get Txp index
    mysession = SQLSession(Schemas.qsar_schema).get_session()

    query3 = mysession.query(Descriptors.index_number, Descriptors.descriptors_name).filter(Descriptors.fk_descriptor_set_id == 1445)
    descriptornames = pd.DataFrame(list(query3))

    # sort by TXP number
    sorted = pd.merge(descriptornames, blabla, on='descriptors_name')
    sorted = sorted.drop('index_number', axis=1)
    # print(sorted.head())

    name =  i.split('_')[0]

    from zMisc_Code.DATA_VISUALIZATION.barplot import barplot
    barplot(sorted.iloc[:,1], sorted.iloc[:,0], name)
    plt.tight_layout()
    # plt.show()
    plt.savefig('/home/rlougee/Desktop/images/{}.png'.format(name))

    # _ = sorted.plot( kind='bar', secondary='p-val')



    # radar(sorted)
    # plt.show()