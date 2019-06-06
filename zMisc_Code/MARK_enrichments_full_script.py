import pandas as pd
import sys

from database.session import SQLSession
from database.database_schemas import Schemas
from database.information.TABLES import Tables
from database.dsstox.compounds import Compounds

df1 = pd.read_csv('~/Desktop/Marks_Files/MARKS_DATA_V2/Ori_SC/ori_hitc_inc_single_conc.csv')

print(df1.head())

# mysession = SQLSession(Schemas.information_schema).get_session()
#
# query0 = mysession.query(Compounds.dsstox_compound_id, Compounds.id )\
#         .filter(Compounds.dsstox_compound_id.in_(myinputtable.iloc[:,0]))
#
# query0 = pd.DataFrame(list(query0))
#
# print(query0.head())
#
# sys.exit(0)

for name, value in df1.iteritems():
    if name == 'DSSTox_Substance_Id':
        continue
    # print(name)
    # print(value)
    # df2 = pd.DataFrame(columns=['DSSTox_Substance_Id', 'hitc'])
    mylist2 = []
    row=0
    for i in value:
        if pd.isnull(i) == True:
            row +=1
            continue
        # print(i, df1.loc[row, name], df1.loc[row, 'DSSTox_Substance_Id'])
        # df2.append({'DSSTox_Substance_Id':df1.loc[row, 'DSSTox_Substance_Id'], 'hitc':int(i)}, ignore_index=True)
        # pd.concat([pd.DataFrame([df1.loc[row, 'DSSTox_Substance_Id'], int(i) ], columns=['DSSTox_Substance_Id', 'hitc'])], ignore_index=True)
        mylist2.append((df1.loc[row, 'DSSTox_Substance_Id'], int(i)))

        row += 1
    df2 = pd.DataFrame(mylist2, columns=['DSSTox_Substance_Id', 'hitc'])
    # print(df2.shape)
    # print(df2.head())
    df2.to_csv("~/Desktop/Marks_Files/MARKS_DATA_V2/Ori_SC/split/{}.tsv".format(name) , sep='\t', index=False)

