import glob
import pandas as pd
from database.database_schemas import Schemas
from database.dsstox.compounds import Compounds
from database.qsar.compound_descriptor_sets import CompoundDescriptorSets
from database.session import SQLSession
import sys

for f in glob.glob("/home/rlougee/Desktop/invitrodb_v2_burst_splits/clean_assays/*"):
    aeid = f.split('/')[-1]
    a = pd.read_csv(f, sep='\t')



    mysession = SQLSession(Schemas.qsar_schema).get_session()

    query0 = mysession.execute('SELECT assay_component_endpoint_name FROM sbox_rlougee_invitrodb.assay_component_endpoint WHERE sbox_rlougee_invitrodb.assay_component_endpoint.aeid = {}'.format(aeid))

    output_name = list(query0)[0][0]
    a = a.dropna(axis=1)
    a.to_csv('/home/rlougee/Desktop/invitrodb_v2_burst_splits/clean_assays2/{}.tsv'.format(output_name), sep='\t', index=False)