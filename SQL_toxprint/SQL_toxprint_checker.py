from database.database_schemas import Schemas
from database.dsstox.compounds import Compounds
from database.qsar.compound_descriptor_sets import CompoundDescriptorSets
from database.session import SQLSession
import sys
import click
import pandas as pd

########################################################################################################################

## TAKES A LIST OF IDS, QUERIES THE DATABASE FOR TOXPRINTS TO SEE IF THEY EXIST
## Start from DTXCID

def check(f):
    mysession = SQLSession(Schemas.qsar_schema).get_session()

    # get all dtxcids
    # remove blacklist here with NOT LIKE '%|%'
    df1 = pd.DataFrame(list(mysession.execute('SELECT compounds.id, compounds.dsstox_compound_id FROM ro_stg_dsstox.compounds WHERE compounds.smiles NOT LIKE "%|%"' )))
    l0 = df1[1].tolist()
    l1 = df1[0].tolist()

    # get all compound ids with toxprints
    l2 = [i[0] for i in list(mysession.execute('SELECT efk_dsstox_compound_id FROM sbox_rlougee_qsar.compound_descriptor_sets WHERE fk_descriptor_set_id = 1445'))]

    # find difference between ids
    l3 = list(set(l1)-set(l2))

    # merge df1 l3
    df2 = pd.merge(pd.DataFrame(l3), df1, on=[0], how='left')
    l4 = list(df2[1])

### IF QSAR.COMPOUND_DESCRIPTOR_SETS IS MISSING EITHER THEN GENERATE TOXPRINTS FOR THIS COMPOUND ###
    if not l4 and f == False:
        print('SQL query is empty: All toxprints available or no DTXCIDs')
        sys.exit(0)
    elif not l4 and f == True:
        return [], l0
    else:
        return l4, l0
