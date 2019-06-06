from database.database_schemas import Schemas
from database.dsstox.compounds import Compounds
from database.session import SQLSession
from database.qsar.compound_descriptor_sets import CompoundDescriptorSets
from database.qsar.descriptors import Descriptors
import sys
import pandas as pd
from io import StringIO
import scipy.stats as stats


def getenrichfp(DataSetName, sigtxp, mypath, myfilename, dsi=1445):
    """ Get Enrichment data for a combined set of chemotypes """

    # aborts if no significant chemotypes
    if len(sigtxp) == 0:
        return None

    mysession = SQLSession(Schemas.qsar_schema).get_session()
    MyDataSet = mysession.execute(
        'SELECT dsstox_compound_id, measured_value_dn, descriptor_string_tsv FROM sbox_rlougee_qsar.datasets'
        ' JOIN sbox_rlougee_qsar.dataset_datapoints ON sbox_rlougee_qsar.dataset_datapoints.fk_dataset_id = sbox_rlougee_qsar.datasets.id'
        ' JOIN sbox_rlougee_qsar.datapoints ON sbox_rlougee_qsar.datapoints.id = sbox_rlougee_qsar.dataset_datapoints.fk_datapoint_id'
        ' JOIN ro_stg_dsstox.compounds ON sbox_rlougee_qsar.datapoints.efk_dsstox_compound_id = ro_stg_dsstox.compounds.id'
        ' JOIN sbox_rlougee_qsar.compound_descriptor_sets ON ro_stg_dsstox.compounds.id = sbox_rlougee_qsar.compound_descriptor_sets.efk_dsstox_compound_id'
        ' WHERE sbox_rlougee_qsar.datasets.name LIKE \'%{}%\' AND sbox_rlougee_qsar.compound_descriptor_sets.fk_descriptor_set_id = {}'.format(DataSetName, dsi))
    MyDataSet = pd.DataFrame(list(MyDataSet))

    MyDataSet.columns = ['Dsstox_Compound_ID', 'Hit_Call', 'Toxprint']

    #something to separate and name fingerprint columns
    MyDataSet = pd.concat([MyDataSet, MyDataSet['Toxprint'].str[:].str.split('\t', expand=True)], axis=1)
    MyDataSet = MyDataSet.drop('Toxprint', axis=1)

    #name the columns correctly
    query3 = mysession.query(Descriptors.descriptors_name, Descriptors.label).filter(Descriptors.fk_descriptor_set_id == dsi)
    descriptornames = pd.DataFrame(list(query3))

    for num,name in enumerate(descriptornames['label'], start=0):
        MyDataSet = MyDataSet.rename(columns={num:name})

    # drop columns that are not significant
    sigtxp = pd.DataFrame(sigtxp)
    sigtxp.columns = ['descriptors_name']
    siglabel = pd.merge(sigtxp, descriptornames, on='descriptors_name', how='inner')
    siglabel = list(siglabel['label'])

    for i in MyDataSet.columns[2:]:
        if i in siglabel:
            pass
        else:
            MyDataSet = MyDataSet.drop(i, axis=1)

    # MyDataSet.to_csv('{}{}.tsv'.format(mypath, myfilename), sep='\t', index=False)

    # return overall balanced accuracy calculations
    # can just make a unique confusion matrix for significant toxprints and add to CT-Enriched Stats file
    # print(MyDataSet.head())
    model_row = pd.DataFrame([['Chemotype Full Model Coverage', myfilename, " ".join(sigtxp['descriptors_name']), 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]], columns = ['Chemotype ID','Data Table','Chemotype Label','Total Chemotypes','True Positives','False Positives','False Negatives','True Negatives','Balanced Accuracy','Odds Ratio','P-Value','Inverse Odds Ratio','Inverse P-Value'])

    # fill model_row confusion matrix
    for index, row in MyDataSet.iterrows():
        rowsum = sum([int(x) for x in row.iloc[2:]])
        if row['Hit_Call'] == 1 and rowsum > 0:
            model_row['True Positives'] += 1
        elif row['Hit_Call'] == 1 and rowsum == 0:
            model_row['False Negatives'] += 1
        elif row['Hit_Call'] == 0 and rowsum > 0:
            model_row['False Positives'] += 1
        elif row['Hit_Call'] == 0 and rowsum == 0:
            model_row['True Negatives'] += 1

    # fill model_row statistics
    oddsratio, pvalue = stats.fisher_exact([ [int(model_row['True Positives']), int(model_row['False Positives'])], [int(model_row['False Negatives']), int(model_row['True Negatives'])]], alternative='greater')
    model_row['P-Value'] = pvalue
    model_row['Odds Ratio'] = oddsratio
    model_row['Total Chemotypes'] = (model_row['True Positives'] + model_row['False Positives'])
    BA = (((model_row['True Positives'] / (model_row['True Positives'] + model_row['False Negatives'])) + (model_row['True Negatives'] / (model_row['True Negatives'] + model_row['False Positives']))) / 2)
    model_row['Balanced Accuracy'] = float(BA)
    inv_oddsratio, inv_pvalue = stats.fisher_exact([ [int(model_row['False Positives']), int(model_row['True Positives'])], [int(model_row['True Negatives']), int(model_row['False Negatives'])] ],alternative='greater')
    model_row['Inverse P-Value'] = inv_pvalue
    model_row['Inverse Odds Ratio'] = inv_oddsratio

    # print(model_row)
    return model_row

# # # # TEST # # #
if __name__ == '__main__':
    # getenrichfp('%NIS\_e1k\_hitcall\_20\_RAIU\_threshold\_hit1\_%',['Txp-1', 'Txp-2', 'Txp-541'] ,'~/Desktop/','TEST', 1445)
    a = getenrichfp("Imported\_DataTable:NIS\_e1k\_hitcall\_20\_RAIU\_threshold\_hit1\_%",
                ["Txp-108", "Txp-109", "Txp-134", "Txp-141", "Txp-142", "Txp-144", "Txp-146", "Txp-153", "Txp-154",
                 "Txp-155", "Txp-158", "Txp-160", "Txp-161", "Txp-166", "Txp-167", "Txp-171", "Txp-179", "Txp-184",
                 "Txp-237", "Txp-239", "Txp-260", "Txp-263", "Txp-264", "Txp-268", "Txp-276", "Txp-280", "Txp-282",
                 "Txp-287", "Txp-32", "Txp-324", "Txp-326", "Txp-338", "Txp-340", "Txp-342", "Txp-471", "Txp-474",
                 "Txp-479", "Txp-488", "Txp-490", "Txp-5", "Txp-614", "Txp-648", "Txp-689", "Txp-691"],
                '/home/rlougee/Desktop/', 'consensus_row_test.txt')


    b = getenrichfp("Imported\_DataTable:NIS\_e1k\_hitcall\_20\_RAIU\_threshold\_hit2\_%",
                ["Txp-117", "Txp-13", "Txp-134", "Txp-137", "Txp-139", "Txp-140", "Txp-142", "Txp-146", "Txp-153", "Txp-154", "Txp-155", "Txp-161", "Txp-166", "Txp-169", "Txp-170", "Txp-183", "Txp-184", "Txp-239", "Txp-260", "Txp-423", "Txp-433", "Txp-557", "Txp-6"  ],
                '/home/rlougee/Desktop/', 'consensus_row_test.txt')
    a.to_csv('{}{}.tsv'.format('/home/rlougee/Desktop/', "JUN_consensus_e1k_prediction_hit1.tsv"), sep='\t', index=False)
    b.to_csv('{}{}.tsv'.format('/home/rlougee/Desktop/', "JUN_consensus_e1k_prediction_hit2.tsv"), sep='\t', index=False)