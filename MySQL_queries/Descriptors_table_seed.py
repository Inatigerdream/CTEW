from database.database_schemas import Schemas
from database.qsar.descriptors import Descriptors
from database.session import SQLSession

import pandas as pd

########################################################################################################################

def filldatabase(yourlist):
    username = 'rlougee'
    descriptors_index = 1445
    mysession = SQLSession(Schemas.qsar_schema).get_session()

    descriptor_objects = []
    for index, val in enumerate(yourlist):

        fk_descriptor_set_id = descriptors_index
        index_number = index+1
        # xx = [str(x) for x in list(row)]
        descriptors_name = 'Txp-{}'.format(index+1)
        created_by = username
        updated_by = username
        long_description = ''
        short_description = ''
        label = val
        descriptor = Descriptors(index_number=index_number, descriptors_name=descriptors_name, long_description=long_description, short_description=short_description, label=label,created_by=created_by,
                                                  fk_descriptor_set_id=fk_descriptor_set_id, updated_by=updated_by)
        descriptor_objects.append(descriptor)
    mysession.bulk_save_objects(descriptor_objects)
    mysession.commit()


####################################################################################################################

mytable = pd.read_csv('~/Desktop/truncated_table.tsv', sep='\t')

mytable = list(mytable.columns.values[2:-2])


filldatabase(mytable)