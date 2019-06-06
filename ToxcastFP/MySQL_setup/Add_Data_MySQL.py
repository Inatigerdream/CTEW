from database.database_schemas import Schemas
from database.session import SQLSession
from database.qsar.descriptors import Descriptors
import sys
import os
import pandas as pd
import datetime


# THIS CODE IS TO BE USED ONE TIME TO FILL sbox_rlougee_qsar.descriptors table for the fingerprint labels, ids, MySQL_setup

# add Toxcast fingerprint data to MySQL
# query AEID data
mysession = SQLSession(Schemas.qsar_schema).get_session()
aeid_data = mysession.execute('SELECT aeid, assay_component_endpoint_name FROM invitrodb.assay_component_endpoint')

aeid_data = pd.DataFrame(list(aeid_data))
aeid_data[0] = [int(x) for x in aeid_data[0] ]
aeid_data = aeid_data.sort_values(0, axis=0)

aeid_data = aeid_data.reset_index(drop=True)
# print(aeid_data)
# sys.exit(1)



# add ASSAY_COMPONENT_ENDPOINT_NAME as descriptors.label
# use aeid as descriptors_name

for i, row in aeid_data.iterrows():
    username = 'rlougee'
    # create a new datasets name entry

    description = "Hit Calls from MC5 for the toxcast AEID: {} taken on the date:{}" \
        .format(row[0], datetime.datetime.today().strftime("%Y%m%d"))


    descriptors = Descriptors(fk_descriptor_set_id='1449', index_number=str(i+1),
                        descriptors_name='AEID-{}'.format(row[0]), label= row[1], updated_by=username, created_by=username,
                        long_description=description, short_description=description)
    mysession.add(descriptors)
    # mysession.flush()
    # fk_dataset_id = int(datasets.id)

    mysession.commit()
    # sys.exit(1)