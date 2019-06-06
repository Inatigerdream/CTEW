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

def updatedatabase(fingerprintdf):
    username = 'rlougee'
    descriptors_index = 1448

    # Query for compound_descriptor_sets.id
    mysession = SQLSession(Schemas.qsar_schema).get_session()

    query3 = mysession.query(Compounds.dsstox_compound_id, CompoundDescriptorSets.id) \
        .join(CompoundDescriptorSets, Compounds.id == CompoundDescriptorSets.efk_dsstox_compound_id).filter(CompoundDescriptorSets.fk_descriptor_set_id == descriptors_index)

    df3 = pd.DataFrame(list(query3))

    #join query with fingerprintdf

    mytable = pd.merge(df3, fingerprintdf, on='dsstox_compound_id')

    # # # CODE FOR UPDATING # # #
    for index, row in mytable.iterrows():
        id = row[1]
        descriptor_string_tsv = row[2]
        updated_by = username
        mysession.query(CompoundDescriptorSets.id, CompoundDescriptorSets.descriptor_string_tsv, CompoundDescriptorSets.updated_by).filter(CompoundDescriptorSets.id == id).update({"descriptor_string_tsv": descriptor_string_tsv, "updated_by": updated_by})
        mysession.commit()

# #TEST#
# if __name__=='__main__':
#     updatedatabase(pd.DataFrame(pd.DataFrame([['DTXCID001000007', '7230331', '011']], columns=['dsstox_compound_id', 'id', 'Special Toxprints'])))

