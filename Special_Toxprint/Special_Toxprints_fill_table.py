from database.database_schemas import Schemas
from database.qsar.compound_descriptor_sets import CompoundDescriptorSets
from database.session import SQLSession

import pandas as pd

########################################################################################################################

### TAKES A TOXPRINTS DATAFRAME AND FILLS QSAR.COMPOUND_DESCRIPTOR_SETS ###
def filldatabase(fingerprintdf):
    mysession = SQLSession(Schemas.qsar_schema).get_session()

    username = 'rlougee'
    descriptors_index = 1448

    compound_descriptor_set_objects = []

    # print(fingerprintdf)

    for index, row in fingerprintdf.iterrows():

        efk_dsstox_compound_id = row[0].split('0',1)[1]
        fk_descriptor_set_id = descriptors_index
        xx = [str(x) for x in list(row[1])]
        descriptor_string_tsv = '\t'.join(xx)
        created_by = username
        updated_by = username
        compound_descriptor_sets = CompoundDescriptorSets(efk_dsstox_compound_id=efk_dsstox_compound_id,
                                                  descriptor_string_tsv=descriptor_string_tsv, created_by=created_by,
                                                  fk_descriptor_set_id=fk_descriptor_set_id, updated_by=updated_by)
        compound_descriptor_set_objects.append(compound_descriptor_sets)
    mysession.bulk_save_objects(compound_descriptor_set_objects)
    mysession.commit()

## TEST ##
# if __name__ == '__main__':
#     filldatabase(pd.DataFrame([['DTXCID01001969', '0' ]], index=[0]))


