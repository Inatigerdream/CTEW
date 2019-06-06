from database.database_schemas import Schemas
from database.qsar.descriptors import Descriptors
from database.session import SQLSession

import pandas as pd

########################################################################################################################

def filldatabase(yourlist, desc_set_id, prefix):
    username = 'rlougee'
    descriptors_index = desc_set_id
    mysession = SQLSession(Schemas.qsar_schema).get_session()

    descriptor_objects = []
    for index, val in enumerate(yourlist):

        fk_descriptor_set_id = descriptors_index
        index_number = index+1
        # xx = [str(x) for x in list(row)]
        descriptors_name = str(prefix.format(index+1))
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

mytable = pd.read_csv('~/Downloads/MACCS_descriptor_info.tsv', sep='\t', header=None)
mytable2 = pd.read_csv('~/Downloads/pubchem_descriptor_info.tsv', sep='\t', header=None)

# mytable = list(mytable.iloc[1,:])
# mytable2 = list(mytable.iloc[1,:])

print(mytable[1][0:166])
# print(mytable2[1])


filldatabase(mytable[1][0:166], int(1446), 'MACCS-{}')
# filldatabase(mytable2[1], int(1447), 'Pubchem-{}')