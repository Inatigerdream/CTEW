from PIL import Image
from AssaySpaceIdentifier import assayspaceidentifier
from ImageMaker import imagemaker
from fpenrich import getenrichfp
from docopt import docopt
from database.database_schemas import Schemas
from database.session import SQLSession
import sys
import os
import pandas as pd
from colorama import init, Fore

mysession = SQLSession(Schemas.qsar_schema).get_session()
enrichment_data_1 = mysession.execute(
    'SELECT datasets.name, descriptors.descriptors_name, descriptors.label, GROUP_CONCAT(CASE WHEN abbreviation = \'CT-Total\' THEN value ELSE NULL END) as \'CT-Tot\',GROUP_CONCAT(CASE WHEN abbreviation = \'TP\' THEN value ELSE NULL END) as \'TP\',GROUP_CONCAT(CASE WHEN abbreviation = \'FP\' THEN value ELSE NULL END) as \'FP\', GROUP_CONCAT(CASE WHEN abbreviation = \'FN\' THEN value ELSE NULL END) as \'FN\', GROUP_CONCAT(CASE WHEN abbreviation = \'TN\' THEN value ELSE NULL END) as \'TN\', GROUP_CONCAT(CASE WHEN abbreviation = \'BA\' THEN value ELSE NULL END) as \'BA\', GROUP_CONCAT(CASE WHEN abbreviation = \'OR\' THEN value ELSE NULL END) as \'OR\', GROUP_CONCAT(CASE WHEN abbreviation = \'P-Val\' THEN value ELSE NULL END) as \'P-Val\', GROUP_CONCAT(CASE WHEN abbreviation = \'Inv OR\' THEN value ELSE NULL END) as \'Inv OR\',GROUP_CONCAT(CASE WHEN abbreviation = \'Inv P-Val\' THEN value ELSE NULL END) as \'Inv P-Val\' FROM sbox_rlougee_qsar.datasets JOIN sbox_rlougee_qsar.univariate_calculations ON sbox_rlougee_qsar.univariate_calculations.fk_dataset_id = sbox_rlougee_qsar.datasets.id JOIN sbox_rlougee_qsar.uc_statistics ON sbox_rlougee_qsar.uc_statistics.fk_univ_calc_id = sbox_rlougee_qsar.univariate_calculations.id JOIN sbox_rlougee_qsar.statistics ON sbox_rlougee_qsar.statistics.id = sbox_rlougee_qsar.uc_statistics.fk_statistic_id JOIN sbox_rlougee_qsar.descriptors ON sbox_rlougee_qsar.descriptors.id = sbox_rlougee_qsar.univariate_calculations.fk_descriptor_id WHERE datasets.name LIKE \'%aeid\_9\_invitrodbv2%\' AND fk_descriptor_set_id = 1445 GROUP BY datasets.name, descriptors.descriptors_name, descriptors.label')

ed1 = pd.DataFrame(list(enrichment_data_1))

ed1.columns = ['Data Table', 'Chemotype ID', 'Chemotype Label', 'Total Chemotypes', 'True Positives', 'False Positives', 'False Negatives', 'True Negatives', 'Balanced Accuracy', 'Odds Ratio', 'P-Value', 'Inverse Odds Ratio', 'Inverse P-Value' ]

# print(pd.DataFrame(list(enrichment_data_1)).head())

enrichment_data_2 = mysession.execute(
    'SELECT datasets.name, descriptors.descriptors_name, descriptors.label, statistics.abbreviation, uc_statistics.value FROM sbox_rlougee_qsar.datasets JOIN sbox_rlougee_qsar.univariate_calculations ON sbox_rlougee_qsar.univariate_calculations.fk_dataset_id = sbox_rlougee_qsar.datasets.id JOIN sbox_rlougee_qsar.uc_statistics ON sbox_rlougee_qsar.uc_statistics.fk_univ_calc_id = sbox_rlougee_qsar.univariate_calculations.id JOIN sbox_rlougee_qsar.statistics ON sbox_rlougee_qsar.statistics.id = sbox_rlougee_qsar.uc_statistics.fk_statistic_id JOIN sbox_rlougee_qsar.descriptors ON sbox_rlougee_qsar.descriptors.id = sbox_rlougee_qsar.univariate_calculations.fk_descriptor_id WHERE datasets.name LIKE \'%aeid\_9\_invitrodbv2%\' AND fk_descriptor_set_id = 1445 GROUP BY datasets.name, descriptors.descriptors_name, descriptors.label, statistics.abbreviation, uc_statistics.value')

ed2 = pd.DataFrame(list(enrichment_data_2))

ed2_2 = pd.pivot_table(ed2, values=4, index=[0,1,2], columns=[3])
ed2_2 = ed2_2.reset_index(level=[0,1,2])

ed2_2.columns = ['Data Table', 'Chemotype ID', 'Chemotype Label','Balanced Accuracy', 'Total Chemotypes','False Negatives', 'False Positives','Inverse Odds Ratio', 'Inverse P-Value',  'Odds Ratio', 'P-Value', 'True Negatives', 'True Positives' ]

ed2_2 = ed2_2[['Data Table', 'Chemotype ID', 'Chemotype Label', 'Total Chemotypes', 'True Positives', 'False Positives', 'False Negatives', 'True Negatives', 'Balanced Accuracy', 'Odds Ratio', 'P-Value', 'Inverse Odds Ratio', 'Inverse P-Value' ]]


print(ed1.head())
print(ed2_2.head())

for i in (ed1 != ed2_2).any(1):
    if i == True:
        print(i)