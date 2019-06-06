from database.database_schemas import Schemas
from database.qsar.compound_descriptor_sets import CompoundDescriptorSets
from database.session import SQLSession

import pandas as pd

########################################################################################################################

### TAKES A TOXPRINTS DATAFRAME AND FILLS QSAR.COMPOUND_DESCRIPTOR_SETS ###

def filldatabase(fingerprintdf):
    username = 'rlougee'
    descriptors_index = 1445
    mysession = SQLSession(Schemas.qsar_schema).get_session()

    compound_descriptor_objects = []
    for index, row in fingerprintdf.iterrows():
        efk_dsstox_compound_id = index[8:]
        fk_descriptor_set_id = descriptors_index
        xx = [str(x) for x in list(row)]
        descriptor_string_tsv = '\t'.join(xx)
        created_by = username
        updated_by = username
        compound_descriptor = CompoundDescriptorSets(efk_dsstox_compound_id=efk_dsstox_compound_id,
                                                  descriptor_string_tsv=descriptor_string_tsv, created_by=created_by,
                                                  fk_descriptor_set_id=fk_descriptor_set_id, updated_by=updated_by)
        compound_descriptor_objects.append(compound_descriptor)
    mysession.bulk_save_objects(compound_descriptor_objects)
    mysession.commit()
