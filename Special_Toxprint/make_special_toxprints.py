from database.database_schemas import Schemas
from database.dsstox.compounds import Compounds
from database.qsar.compound_descriptor_sets import CompoundDescriptorSets
from database.session import SQLSession
import pandas as pd
########################################################################################################################

# # # MAKE THE SPECIAL TOXPRINTS COMBINATIONS # # #

def mk_special_fingerprints(idrow):
    # query existing toxprints
    dsi = 1445
    mysession = SQLSession(Schemas.qsar_schema).get_session()

    query2 = mysession.query(Compounds.dsstox_compound_id, CompoundDescriptorSets.descriptor_string_tsv) \
        .join(CompoundDescriptorSets, Compounds.id == CompoundDescriptorSets.efk_dsstox_compound_id).filter(CompoundDescriptorSets.fk_descriptor_set_id == dsi)
    df2 = pd.DataFrame(list(query2))

    # FILTERING BY A LIST OF >1000 WON'T WORK IN MANY DATABASES (THIS IS BREAKING THE SCRIPT HERE ON FULL UPDATE)
    # doing a full query then a merge after
    df2 = pd.merge(pd.DataFrame(idrow, columns=['dsstox_compound_id']), df2, on='dsstox_compound_id')

    # something to separate and name fingerprint columns
    df2 = pd.concat([df2, df2['descriptor_string_tsv'].str[:].str.split('\t', expand=True)], axis=1)
    df2 = df2.drop('descriptor_string_tsv', axis=1)

    # # # GENERATE SPECIFIC NEW FINGERPRINTS # # #
    # create an empty column for the new fingerprint
    df2['Special_Toxprints'] = ""

    # iterate through datatable and create new Special Toxprints
    # make sure you are looking at the right index when combining Toxprints
    for index, row in df2.iterrows():
        # have to code each special toxprint this way
        if row[480] == '1' and row[489] == '1':
            row['Special_Toxprints'] = '1'
        else:
            row['Special_Toxprints'] = '0'

        # make sure to add tabs before the rest of the toxprints
        if row[489] == '1' and row[480] == '0':
            row['Special_Toxprints'] += '\t1'
        else:
            row['Special_Toxprints'] += '\t0'

        if row[480] == '1' and row[489] == '0':
            row['Special_Toxprints'] += '\t1'
        else:
            row['Special_Toxprints'] += '\t0'

    # remove everything but fingerprints and DTXCIDs
    output_df = df2[['dsstox_compound_id', 'Special_Toxprints']]
    return output_df

# TEST ##
# am i inputting a list just like this?
#
# if __name__ == "__main__":
#     mylist = ['DTXCID001030', 'DTXCID0012344', 'DTXCID0012390', 'DTXCID0012392',
#               'DTXCID0012398', 'DTXCID0012500', 'DTXCID0012502', 'DTXCID0012552',
#               'DTXCID0012637', 'DTXCID001336']
#     print(mk_special_fingerprints(mylist))

