import matplotlib.pyplot as plt
import pandas as pd

from database.database_schemas import Schemas
from database.qsar.descriptors import Descriptors
from database.session import SQLSession
from zMisc_Code.DATA_VISUALIZATION.barplot import barplot

mysession = SQLSession(Schemas.qsar_schema).get_session()

query3 = mysession.query(Descriptors.index_number, Descriptors.descriptors_name).filter(
    Descriptors.fk_descriptor_set_id == 1445)
descriptornames = pd.DataFrame(list(query3))

wow = pd.read_csv("/home/rlougee/Desktop/Assay_Categories/enrichment_tables/intended_target_family_sub_steroidal_table.tsv", sep='\t')

wow['descriptors_name'] = wow['Fingerprint_ID']
print(wow.head())

sorted = pd.merge(descriptornames, wow, on='descriptors_name', how='outer')
wow = sorted.drop(['index_number', 'Fingerprint_ID', 'F-Total', 'TP', 'FP', 'FN', 'TN', 'Balanced Accuracy'], axis=1)
print(wow.head())



barplot(wow.iloc[:, 1], wow.iloc[:, 0], "Intended Target Steroidal Assays")
plt.tight_layout()
plt.show()
# plt.savefig('/home/rlougee/Desktop/images/{}.png'.format(name))
