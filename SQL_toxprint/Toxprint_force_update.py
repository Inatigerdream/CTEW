from database.database_schemas import Schemas
from database.qsar.compound_descriptor_sets import CompoundDescriptorSets
from database.session import SQLSession
from database.dsstox.compounds import Compounds
import pandas as pd
from sqlalchemy.sql.expression import bindparam
from sqlalchemy import update
import sys
########################################################################################################################

### TAKES A TOXPRINTS DATAFRAME AND FILLS QSAR.COMPOUND_DESCRIPTOR_SETS ###

def update_toxprint_database(fingerprintdf):
    username = 'rlougee'
    descriptors_index = 1445

    # Query for compound_descriptor_sets.id
    mysession = SQLSession(Schemas.qsar_schema).get_session()

    query3 = mysession.query(CompoundDescriptorSets.id, CompoundDescriptorSets.efk_dsstox_compound_id)\
        .filter(CompoundDescriptorSets.fk_descriptor_set_id == descriptors_index)

    df3 = pd.DataFrame(list(query3))

    #join query with fingerprintdf
    fingerprintdf = fingerprintdf.reset_index()
    fingerprintdf = fingerprintdf.rename(columns = {'M_NAME':'efk_dsstox_compound_id'}) # not sure this will work
    fingerprintdf['efk_dsstox_compound_id'] = [int(x[8:]) for x in fingerprintdf['efk_dsstox_compound_id']]
    mytable = pd.merge(df3, fingerprintdf, on='efk_dsstox_compound_id')

    # # # CODE FOR UPDATING # # #
    for index, row in mytable.iterrows():
        id = str(row[0])
        xx = [str(x) for x in list(row[2:])]
        descriptor_string_tsv = '\t'.join(xx)
        updated_by = username
        mysession.query(CompoundDescriptorSets.id, CompoundDescriptorSets.descriptor_string_tsv, CompoundDescriptorSets.updated_by).filter(CompoundDescriptorSets.id == id).update({"descriptor_string_tsv": descriptor_string_tsv, "updated_by": updated_by})
        mysession.commit()

# #TEST#
# if __name__=='__main__':
#     df = pd.DataFrame(pd.DataFrame([[1030,0,1,1,0,1,1,1,0,0,1,0]], columns=[0, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']))
#     df = df.set_index(0)
#     updatedatabase(df)

